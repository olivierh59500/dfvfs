#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2013 The PyVFS Project Authors.
# Please see the AUTHORS file for details on individual authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The operating system file entry implementation."""

import os

from pyvfs.io import os_file
from pyvfs.vfs import file_entry
from pyvfs.vfs import stat


class _OSDirectory(object):
  """The operating system directory object implementation."""

  def __init__(self, location):
    """Initializes the directory object.

    Args:
      location: the location of the directory.
    """
    self._location = location
    self._entries = None

  def _GetEntries(self):
    """Retrieves the entries."""
    return os.listdir(self._location)

  @property
  def number_of_entries(self):
    """The number of entries."""
    if self._entries is None:
      self._entries = self._GetEntries()
    return len(self._entries)

  @property
  def entries(self):
    """The entries."""
    if self._entries is None:
      self._entries = self._GetEntries()
    return self._entries


class OSFileEntry(file_entry.FileEntry):
  """The operating system file entry implementation."""

  def __init__(self, path_spec, file_system):
    """Initializes the file entry object.

    Args:
      file_system: the file system object (instance of vfs.FileSystem).
      path_spec: the path specification object (instance of path.PathSpec).
    """
    super(OSFileEntry, self).__init__(file_system, path_spec)
    self._stat_object = None

  def _GetDirectory(self):
    """Retrieves the directory object (instance of _OSDirectory)."""
    if self._stat_object is None:
      self._stat_object = self._GetStat()

    if self._stat_object and self._stat_object.IsDirectory():
      location = getattr(self.path_spec, 'location', None)

      if location is None:
        return None
      return _OSDirectory(location)
    return None

  def _GetStat(self):
    """Retrieves the stat object (instance of vfs.Stat)."""
    location = getattr(self.path_spec, 'location', None)

    if location is None:
      return None

    stat_info = os.stat(location)
    stat_object = stat.Stat()

    # File data stat information.
    stat_object.size = stat_info.st_size

    # Date and time stat information.
    stat_object.atime = stat_info.st_atime
    stat_object.ctime = stat_info.st_ctime
    stat_object.mtime = stat_info.st_mtime

    # Ownership and permissions stat information.
    stat_object.mode = stat.S_IMODE(stat_info.st_mode)
    stat_object.uid = stat_info.st_uid
    stat_object.gid = stat_info.st_gid

    # File entry type stat information.
    if stat.S_ISDIR(stat_info.st_mode):
      stat_object.type = stat_object.TYPE_DIRECTORY
    elif stat.S_ISLNK(stat_info.st_mode):
      stat_object.type = stat_object.TYPE_LINK
    elif (stat.S_ISCHR(stat_info.st_mode) or
          stat.S_ISBLK(stat_info.st_mode)):
      stat_object.type = stat_object.TYPE_DEVICE
    elif stat.S_ISREG(stat_info.st_mode):
      stat_object.type = stat_object.TYPE_FILE
    elif stat.S_ISFIFO(stat_info.st_mode):
      stat_object.type = stat_object.TYPE_PIPE
    elif stat.S_ISSOCK(stat_info.st_mode):
      stat_object.type = stat_object.TYPE_SOCKET

    # Other stat information.
    # stat_object.ino = stat_info.st_ino
    # stat_object.dev = stat_info.st_dev
    # stat_object.nlink = stat_info.st_nlink
    stat_object.fs_type = 'Unknown'
    stat_object.allocated = True

    return stat_object

  @property
  def name(self):
    """The name."""
    location = getattr(self.path_spec, 'location', '')
    return os.path.basename(location)

  @property
  def number_of_sub_file_entries(self):
    """The number of sub file entries."""
    if self._directory is None:
      self._directory = self._GetDirectory()

    if self._directory:
      return self._directory.number_of_entries
    return 0

  @property
  def sub_file_entries(self):
    """The sub file entries."""
    if self._directory is None:
      self._directory = self._GetDirectory()

    if self._directory:
      return self._directory.number_of_entries
    return []

  def GetData(self):
    """Retrieves the file-like object (instance of io.FileIO) of the data."""
    file_object = os_file.OSFile()
    file_object.open(self.path_spec)
    return file_object

  def GetStat(self):
    """Retrieves the stat object (instance of vfs.Stat)."""
    if self._stat_object is None:
      self.GetStat()
    return self._stat_object
