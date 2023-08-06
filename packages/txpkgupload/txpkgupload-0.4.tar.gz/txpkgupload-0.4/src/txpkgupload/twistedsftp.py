# Copyright 2010-2011 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Twisted SFTP implementation of the txpkgupload upload server."""

__metaclass__ = type
__all__ = [
    'SFTPFile',
    'SFTPServer',
    ]

import errno
import os
import tempfile

from lazr.sshserver.sftp import (
    FileIsADirectory,
    FileTransferServer,
    )
from twisted.conch.interfaces import (
    ISFTPFile,
    ISFTPServer,
    )
from zope.interface import implementer

from txpkgupload.filesystem import UploadFileSystem
from txpkgupload.hooks import Hooks


@implementer(ISFTPServer)
class SFTPServer:
    """An implementation of `ISFTPServer` that backs onto a txpkgupload fs."""

    def __init__(self, avatar):
        self._avatar = avatar
        self._fs_root = avatar.fs_root
        self.uploadfilesystem = UploadFileSystem(
            tempfile.mkdtemp(dir=avatar.temp_dir))
        self._current_upload = self.uploadfilesystem.rootpath
        os.chmod(self._current_upload, 0o770)

    def gotVersion(self, other_version, ext_data):
        return {}

    def openFile(self, filename, flags, attrs):
        self._create_missing_directories(filename)
        absfile = self._translate_path(filename)
        return SFTPFile(absfile)

    def removeFile(self, filename):
        pass

    def renameFile(self, old_path, new_path):
        abs_old = self._translate_path(old_path)
        abs_new = self._translate_path(new_path)
        os.rename(abs_old, abs_new)

    def makeDirectory(self, path, attrs):
        # XXX: We ignore attrs here
        self.uploadfilesystem.mkdir(path)

    def removeDirectory(self, path):
        self.uploadfilesystem.rmdir(path)

    def openDirectory(self, path):
        return SFTPDirectory()

    def getAttrs(self, path, follow_links):
        return {}

    def setAttrs(self, path, attrs):
        pass

    def readLink(self, path):
        pass

    def makeLink(self, link_path, target_path):
        pass

    def realPath(self, path):
        return path

    def extendedRequest(self, extended_name, extended_data):
        pass

    def _create_missing_directories(self, filename):
        new_dir, new_file = os.path.split(
            self.uploadfilesystem._sanitize(filename))
        if new_dir != '':
            if not os.path.exists(
                os.path.join(self._current_upload, new_dir)):
                self.uploadfilesystem.mkdir(new_dir)

    def _translate_path(self, filename):
        return self.uploadfilesystem._full(
            self.uploadfilesystem._sanitize(filename))


@implementer(ISFTPFile)
class SFTPFile:

    def __init__(self, filename):
        self.filename = filename

    def close(self):
        pass

    def readChunk(self, offset, length):
        pass

    def writeChunk(self, offset, data):
        try:
            chunk_file = os.open(
                self.filename, os.O_CREAT | os.O_WRONLY, 0o644)
        except OSError as e:
            if e.errno != errno.EISDIR:
                raise
            raise FileIsADirectory(self.filename)
        os.lseek(chunk_file, offset, 0)
        os.write(chunk_file, data)
        os.close(chunk_file)

    def getAttrs(self):
        return {}

    def setAttrs(self, attr):
        pass


class SFTPDirectory:

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration

    next = __next__

    def close(self):
        pass


class PkgUploadFileTransferServer(FileTransferServer):

    def __init__(self, data=None, avatar=None):
        FileTransferServer.__init__(self, data=data, avatar=avatar)
        self.hook = Hooks(self.client._fs_root, perms='g+rws', prefix='-sftp')
        self.hook.new_client_hook(self.client._current_upload, 0, 0)

    def connectionLost(self, reason):
        if self.hook is not None:
            self.hook.client_done_hook(self.client._current_upload, 0, 0)
            self.hook = None
