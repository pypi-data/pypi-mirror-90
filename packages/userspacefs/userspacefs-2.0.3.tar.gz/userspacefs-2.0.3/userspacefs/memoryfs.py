#!/usr/bin/env python3

# This file is part of userspacefs.

# userspacefs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# userspacefs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with userspacefs.  If not, see <http://www.gnu.org/licenses/>.

import codecs
import collections
import ctypes
import errno
import io
import itertools
import json
import logging
import os
import threading
import warnings

from datetime import datetime

from userspacefs.path_common import Path
from userspacefs.util_dumpster import PositionIO, null_context, quick_container

log = logging.getLogger(__name__)

def get_size(md):
    if md["type"] == "directory":
        return 0
    else:
        assert md["type"] == "file"
        return len(md.get("data", b''))

def get_children(md):
    assert md["type"] == "directory"
    return md.get("children", [])

def get_rev(md):
    if md['type'] == 'directory':
        return None
    else:
        return 'rev:' + codecs.encode(json.dumps((id(md), len(md['revs']) - 1)).encode('utf-8'), 'hex').decode('ascii')

def decode_rev(rev):
    if not rev.startswith('rev:'):
        raise ValueError("bad rev!")
    return json.loads(codecs.decode(rev[4:].encode('ascii'), 'hex').decode('utf-8'))

def get_id(md):
    return 'id:' + str(id(md))

class _File(PositionIO):
    def __init__(self, md, mode):
        super().__init__()

        self._md = md
        self._mode = mode

    def pread(self, size, offset):
        if not self.readable():
            raise OSError(errno.EBADF, os.strerror(errno.EBADF))
        if self._md["type"] == "directory":
            raise OSError(errno.EISDIR, os.strerror(errno.EISDIR))
        d = self._md["data"]
        return d[offset:
                 len(d) if size < 0 else offset + size]

    def readable(self):
        return (self._mode & os.O_ACCMODE) in (os.O_RDONLY, os.O_RDWR)

    def _file_length(self):
        return len(self._md["data"])

    def pwrite(self, buf, offset):
        if not self.writable():
            raise OSError(errno.EBADF, os.strerror(errno.EBADF))
        with self._md['lock']:
            header = self._md['data'][:offset]
            if len(header) < offset:
                header = b'%s%s' % (header, b'\0' * (offset - len(header),))
            d = self._md["data"] = b'%s%s%s' % (header, buf,
                                                self._md['data'][offset + len(buf):])
            m = self._md['mtime'] = datetime.utcnow()
            self._md['ctime'] = datetime.utcnow()
            self._md['revs'].append((m, d))
            return len(buf)

    def writable(self):
        return (self._mode & os.O_ACCMODE) in (os.O_WRONLY, os.O_RDWR)

    def ptruncate(self, offset):
        if not self.writable():
            raise OSError(errno.EBADF, os.strerror(errno.EBADF))
        with self._md['lock']:
            if offset <= len(self._md['data']):
                d = self._md["data"] = self._md['data'][:offset]
            else:
                d = self._md["data"] = (self._md['data'] +
                                        b'\0' * (offset - len(self._md['data'])))
            m = self._md['mtime'] = datetime.utcnow()
            self._md['ctime'] = datetime.utcnow()
            self._md['revs'].append((m, d))
            return 0

class _Directory(object):
    def __init__(self, fs, md):
        self._fs = fs
        self._md = md
        self.reset()

    def reset(self):
        # copy list of children, n/s exactly what ext2/POSIX others do
        # in concurrent situations
        with self._md['lock']:
            l = list(get_children(self._md))
        # NB: I apologize if you're about to grep for _map_entry()
        self._iter = iter(map(lambda tup: self._fs._map_entry(tup[1], tup[0]), l))

    def close(self):
        pass

    def read(self):
        try:
            return next(self)
        except StopIteration:
            return None

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iter)

    def readmany(self, size=None):
        if size is None:
            return list(self)
        else:
            return list(itertools.islice(self, size))

ATTRS = ['name', 'mtime', 'type', 'size', 'id', 'ctime', 'rev']
_Stat = collections.namedtuple("Stat", ATTRS + ['attrs'])

class _ReadStream(PositionIO):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def pread(self, size, offset):
        return self._data[offset:
                          len(self._data) if size < 0 else offset + size]

    def readable(self):
        return True

class _WriteStream(object):
    def __init__(self, fs):
        self._fs = fs
        self._buf = io.BytesIO()

    def write(self, data):
        self._buf.write(data)

    def close(self):
        pass

    def finish(self, resolver, mode="add", strict_conflict=False,
               mtime=None):
        # this reads a snapshotted file resolved by resolver
        if isinstance(resolver, Path):
            mode_ = 0
            if mode == "add":
                mode_ = mode_ | os.O_CREAT
                if strict_conflict:
                    mode_ = mode_ | os.O_EXCL
            elif mode == "overwrite":
                mode_ = mode_ | os.O_CREAT
            else:
                assert (isinstance(mode, tuple) and
                        mode[0] == 'update' and
                        mode[1][:4] == 'rev:')

            md = self._fs._get_file(resolver, mode=mode_)
        else:
            assert (isinstance(mode, tuple) and
                    mode[0] == 'update' and
                    mode[1][:4] == 'rev:')

            md = self._fs._md_from_id(resolver)

        if mode == "add":
            if get_size(md):
                raise OSError(errno.EEXIST, os.strerror(errno.EEXIST))
        elif mode == "overwrite":
            pass
        else:
            if ((strict_conflict or get_size(md)) and
                mode[1] != get_rev(md)):
                raise OSError(errno.EEXIST, os.strerror(errno.EEXIST))

        if mtime is None:
            mtime = datetime.utcnow()

        with md['lock']:
            d = md['data'] = self._buf.getvalue()
            m = md['mtime'] = mtime
            c = md['ctime'] = datetime.utcnow()
            md['revs'].append((m, d))
            rev = get_rev(md)
        self._buf.close()

        DropboxMD = collections.namedtuple(
            "DropboxMD",
            ["path_lower", "name", "client_modified",
             "size", "server_modified", "rev", "id"])
        return DropboxMD(path_lower=str(md['path']).lower(),
                         name=md['name'],
                         client_modified=m,
                         size=len(d),
                         server_modified=c,
                         id=get_id(md),
                         rev=rev[4:])

class FileSystem(object):
    def __init__(self, tree=()):
        self._unlinked_files = []
        self._parent = {"type": "directory", "children": [],
                        'lock': threading.Lock(),
                        'mtime': datetime.utcnow(), 'ctime': datetime.utcnow()}

        # give all files a lock
        files = [(self.create_path(),
                  self._parent,
                  {"type": "directory", "children": tree})]
        while files:
            (dir_path, new_dir, dir_) = files.pop()
            for (name, child) in get_children(dir_):
                new_child = dict(child)
                new_child['path'] = dir_path.joinpath(name)
                new_child['name'] = name
                if 'mtime' not in new_child:
                    new_child['mtime'] = datetime.utcnow()
                if 'ctime' not in new_child:
                    new_child['ctime'] = datetime.utcnow()

                new_child['lock'] = threading.Lock()

                if child['type'] == 'file':
                    new_child['revs'] = [(new_child['mtime'], new_child['data'])]
                else:
                    assert child['type'] == 'directory'
                    new_child['children'] = []
                    files.append((new_child['path'], new_child, child))
                new_dir['children'].append((name, new_child))

    def _map_entry(self, md, name=None):
        mtime = md['mtime']
        ctime = md['ctime']
        type = md["type"]
        size = get_size(md)
        rev = get_rev(md)

        return _Stat(name, mtime, type, size, id=get_id(md), ctime=ctime, rev=rev,
                     attrs=ATTRS)

    def _get_file(self, path, mode=0, remove=None, directory=False):
        assert not (remove is not None and mode),\
            "Only one of mode/remove should be specified"
        parent = self._parent
        real_comps = []
        for comp in itertools.islice(path.parts, 1, None):
            if parent["type"] != "directory":
                raise OSError(errno.ENOTDIR, os.strerror(errno.ENOTDIR))

            with parent['lock']:
                for (idx, (name, md)) in enumerate(get_children(parent)):
                    if name.lower() == comp.lower():
                        real_comps.append(name)
                        if len(real_comps) == len(path.parts) - 1:
                            if (mode & os.O_CREAT) and (mode & os.O_EXCL):
                                raise OSError(errno.EEXIST, os.strerror(errno.EEXIST))
                            if remove is not None:
                                if remove == 'unlink':
                                    if md['type'] != 'file':
                                        raise OSError(errno.EPERM, os.strerror(errno.EPERM))
                                elif remove == 'rmdir':
                                    if md['type'] != 'directory':
                                        raise OSError(errno.ENOTDIR, os.strerror(errno.ENOTDIR))
                                    if get_children(md):
                                        raise OSError(errno.ENOTEMPTY, os.strerror(errno.ENOTEMPTY))
                                else:
                                    assert False, "Bad remove value!"
                                del parent['children'][idx]

                        parent = md
                        break
                else:
                    real_comps.append(comp)
                    if (remove is None and
                        len(real_comps) == len(path.parts) - 1 and
                        (mode & os.O_CREAT)):
                        t = datetime.utcnow()
                        if directory:
                            md = dict(type='directory',
                                      children=[],
                                      path=self.create_path(*real_comps),
                                      name=comp,
                                      mtime=t,
                                      ctime=t,
                                      lock=threading.Lock())
                        else:
                            md = dict(type='file',
                                      data=b'',
                                      path=self.create_path(*real_comps),
                                      name=comp,
                                      mtime=t,
                                      ctime=t,
                                      lock=threading.Lock(),
                                      revs=[(t, b'')])
                        parent.setdefault('children', []).append((comp, md))
                        parent = md
                        break
                    raise OSError(errno.ENOENT, os.strerror(errno.ENOENT))

        if mode & os.O_TRUNC and parent['type'] == 'file':
            with parent['lock']:
                parent['data'] = b''
                parent['revs'].append((datetime.utcnow(), b''))

        return parent

    def parse_path(self, path):
        return Path.parse_path(path, fn_norm=self.file_name_norm)

    def create_path(self, *args):
        return Path.root_path(fn_norm=self.file_name_norm).joinpath(*args)

    def file_name_norm(self, fn):
        return fn.lower()

    def open(self, path, mode=os.O_RDONLY, directory=False):
        md = self._get_file(path, mode, directory=directory)
        return _File(md, mode)

    def _low_md_from_id(self, id_):
        warnings.warn("Don't use this in production, could cause segfault if used with an invalid ID")
        return ctypes.cast(id_, ctypes.py_object).value

    def _md_from_id(self, id_):
        if not id_.startswith('id:'):
            raise ValueError("Bad id!")
        id_ = int(id_[3:])
        return self._low_md_from_id(id_)

    def x_open_by_id(self, id_, mode=os.O_RDONLY):
        # id is the memory address of the md object
        return _File(self._md_from_id(id_), mode)

    def x_read_stream(self, resolver, offset=None):
        # this reads a snapshotted file resolved by resolver
        if isinstance(resolver, Path):
            md = self._get_file(resolver)
            rev_idx = None
        else:
            try:
                (md_id, rev_idx) = decode_rev(resolver)
                md = self._low_md_from_id(md_id)
            except ValueError:
                md = self._md_from_id(resolver)
                rev_idx = None

        if rev_idx is None:
            d = md['data']
        else:
            d = md['revs'][rev_idx][1]

        if offset is not None:
            d = d[offset:]

        return _ReadStream(d)

    def x_write_stream(self):
        return _WriteStream(self)

    def open_directory(self, path):
        md = self._get_file(path)
        if md['type'] != "directory":
            raise OSError(errno.ENOTDIR, os.strerror(errno.ENOTDIR))

        return _Directory(self, md)

    def stat_has_attr(self, attr):
        return attr in ["type", "name", "mtime"]

    def x_stat_create(self, path, mode, directory=False):
        return self._map_entry(self._get_file(path, mode & ~os.O_TRUNC, directory=directory))

    def stat(self, path):
        return self.x_stat_create(path, 0)

    def fstat(self, fobj):
        return self._map_entry(fobj._md)

    def create_watch(self, cb, dir_handle, completion_filter, watch_tree):
        if dir_handle._md['type'] != "directory":
            raise OSError(errno.EINVAL, os.strerror(errno.EINVAL))

        # NB: current MemoryFS is read-only so
        #     just wait for stop() is a no-op and cb is never called

        def stop(): pass

        return stop

    def unlink(self, path):
        md = self._get_file(path, remove='unlink')
        # NB: we need to save a reference to the 'inode' of the unlinked file
        #     since there still may still be ID holders (we resolve by object
        #     address)
        self._unlinked_files.append(md)

    def mkdir(self, path):
        st = self._get_file(path, mode=os.O_CREAT | os.O_EXCL, directory='file')
        assert st['type'] == 'directory'

    def rmdir(self, path):
        md = self._get_file(path, remove='rmdir')
        # NB: we need to save a reference to the 'inode' of the unlinked file
        #     since there still may still be ID holders (we resolve by object
        #     address)
        self._unlinked_files.append(md)

    def x_rename_stat(self, old_path, new_path):
        parent = self._get_file(old_path.parent)
        target_parent = self._get_file(new_path.parent)

        if parent['type'] != 'directory' or target_parent['type'] != 'directory':
            raise OSError(errno.ENOTDIR, os.strerror(errno.ENOTDIR))

        if id(parent) == id(target_parent):
            first, second = parent['lock'], null_context()
        elif id(parent) < id(target_parent):
            first, second = parent['lock'], target_parent['lock']
        else:
            first, second = target_parent['lock'], parent['lock']

        with first, second:
            for (name, _) in get_children(target_parent):
                if name.lower() == new_path.name.lower():
                    raise OSError(errno.EEXIST, os.strerror(errno.EEXIST))
            for (idx, (name, md)) in enumerate(get_children(parent)):
                if name.lower() == old_path.name.lower():
                    del parent['children'][idx]
                    break
            else:
                # In the period between the original get_file and now
                # the file was deleted
                raise OSError(errno.ENOENT, os.strerror(errno.ENOENT))

            get_children(target_parent).append((new_path.name, md))

            return self._map_entry(md)

    def rename_noreplace(self, old_path, new_path):
        self.x_rename_stat(old_path, new_path)

    def statvfs(self):
        return quick_container(f_frsize=2 ** 16,
                               f_blocks=2 ** 32 - 1,
                               f_bavail=2 ** 32 - 1)

    def pread(self, handle, size, offset):
        return handle.pread(size, offset)

    def pwrite(self, handle, data, offset):
        return handle.pwrite(data, offset)

    def ftruncate(self, handle, offset):
        return handle.ptruncate(offset)

    def fsync(self, _):
        pass

    def x_f_set_file_times(self, handle, creation_time, last_access_time,
                           last_write_time, change_time):
        if change_time is not None:
            handle._md['ctime'] = change_time
        if last_write_time is not None:
            handle._md['mtime'] = last_write_time

    def close(self):
        pass
