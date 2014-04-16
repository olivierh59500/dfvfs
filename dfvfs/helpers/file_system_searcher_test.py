#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2014 The dfVFS Project Authors.
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
"""Tests for the file system searcher object."""

import os
import unittest

from dfvfs.lib import definitions
from dfvfs.file_io import qcow_file_io
from dfvfs.helpers import file_system_searcher
from dfvfs.path import os_path_spec
from dfvfs.path import qcow_path_spec
from dfvfs.resolver import context
from dfvfs.vfs import os_file_system
from dfvfs.vfs import tsk_file_system


class FileSystemSearcherTest(unittest.TestCase):
  """The unit test for the file system searcher object."""
  maxDiff = None

  def setUp(self):
    """Sets up the needed objects used throughout the test."""
    self._resolver_context = context.Context()
    test_file = os.path.join(os.getcwd(), 'test_data')
    self._os_path_spec = os_path_spec.OSPathSpec(location=test_file)
    self._os_file_system = os_file_system.OSFileSystem(self._resolver_context)

    test_file = os.path.join('test_data', 'vsstest.qcow2')
    path_spec = os_path_spec.OSPathSpec(location=test_file)
    self._qcow_path_spec = qcow_path_spec.QcowPathSpec(parent=path_spec)
    file_object = qcow_file_io.QcowFile(self._resolver_context)
    file_object.open(self._qcow_path_spec)
    self._tsk_file_system = tsk_file_system.TSKFileSystem(
        self._resolver_context, file_object, self._qcow_path_spec)

  def testFind(self):
    """Test the Find() function."""
    searcher = file_system_searcher.FileSystemSearcher(self._tsk_file_system)

    # Find all the file entries of type: FILE_ENTRY_TYPE_FILE.
    find_spec = file_system_searcher.FindSpec(
        file_entry_types=[definitions.FILE_ENTRY_TYPE_FILE])
    path_spec_generator = searcher.Find(find_specs=[find_spec])
    self.assertNotEquals(path_spec_generator, None)

    expected_locations = [
        u'/$AttrDef',
        u'/$BadClus',
        u'/$Bitmap',
        u'/$Boot',
        u'/$Extend/$ObjId',
        u'/$Extend/$Quota',
        u'/$Extend/$Reparse',
        u'/$Extend/$RmMetadata/$Repair',
        u'/$Extend/$RmMetadata/$TxfLog/$Tops',
        u'/$Extend/$RmMetadata/$TxfLog/$TxfLog.blf',
        u'/$Extend/$RmMetadata/$TxfLog/$TxfLogContainer00000000000000000001',
        u'/$Extend/$RmMetadata/$TxfLog/$TxfLogContainer00000000000000000002',
        u'/$LogFile',
        u'/$MFTMirr',
        u'/$Secure',
        u'/$UpCase',
        u'/$Volume',
        u'/another_file',
        u'/password.txt',
        u'/syslog.gz',
        u'/System Volume Information/{3808876b-c176-4e48-b7ae-04046e6cc752}',
        (u'/System Volume Information/{600f0b69-5bdf-11e3-9d6c-005056c00008}'
         u'{3808876b-c176-4e48-b7ae-04046e6cc752}'),
        (u'/System Volume Information/{600f0b6d-5bdf-11e3-9d6c-005056c00008}'
         u'{3808876b-c176-4e48-b7ae-04046e6cc752}')]

    locations = []
    for path_spec in path_spec_generator:
      locations.append(getattr(path_spec, 'location', u''))

    self.assertEquals(locations, expected_locations)

    # Find all the file entries of type: FILE_ENTRY_TYPE_DIRECTORY.
    find_spec = file_system_searcher.FindSpec(
        file_entry_types=[definitions.FILE_ENTRY_TYPE_DIRECTORY])
    path_spec_generator = searcher.Find(find_specs=[find_spec])
    self.assertNotEquals(path_spec_generator, None)

    expected_locations = [
        u'/',
        u'/$Extend',
        u'/$Extend/$RmMetadata',
        u'/$Extend/$RmMetadata/$Txf',
        u'/$Extend/$RmMetadata/$TxfLog',
        u'/System Volume Information',
        u'/$OrphanFiles']

    locations = []
    for path_spec in path_spec_generator:
      locations.append(getattr(path_spec, 'location', u''))

    self.assertEquals(locations, expected_locations)

    # Find all the file entries of type: FILE_ENTRY_TYPE_LINK.
    find_spec = file_system_searcher.FindSpec(
        file_entry_types=[definitions.FILE_ENTRY_TYPE_LINK])
    path_spec_generator = searcher.Find(find_specs=[find_spec])
    self.assertNotEquals(path_spec_generator, None)

    expected_locations = []

    locations = []
    for path_spec in path_spec_generator:
      locations.append(getattr(path_spec, 'location', u''))

    self.assertEquals(locations, expected_locations)

    # Find all the file entries with location:
    # /$Extend/$RmMetadata/$TxfLog/$TxfLog.blf
    find_spec1 = file_system_searcher.FindSpec(
        location=u'/$Extend/$RmMetadata')
    find_spec2 = file_system_searcher.FindSpec(
        location=u'/$Extend/$RmMetadata/$TxfLog/$TxfLog.blf')
    find_spec3 = file_system_searcher.FindSpec(
        location=u'/password.txt')
    path_spec_generator = searcher.Find(
        find_specs=[find_spec1, find_spec2, find_spec3])
    self.assertNotEquals(path_spec_generator, None)

    expected_locations = [
        u'/$Extend/$RmMetadata',
        u'/$Extend/$RmMetadata/$TxfLog/$TxfLog.blf',
        u'/password.txt']

    locations = []
    for path_spec in path_spec_generator:
      locations.append(getattr(path_spec, 'location', u''))

    self.assertEquals(locations, expected_locations)


if __name__ == '__main__':
  unittest.main()
