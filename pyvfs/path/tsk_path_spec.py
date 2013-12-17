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
"""The SleuthKit path specification implementation."""

from pyvfs.path import factory
from pyvfs.path import path_spec


PATH_SEPARATOR = u'/'


class TSKPathSpec(path_spec.PathSpec):
  """Class that implements the SleuthKit path specification."""

  TYPE_INDICATOR = u'TSK'

  def __init__(self, inode=None, location=None, parent=None, **kwargs):
    """Initializes the path specification object.

       The SleuthKit path specification object allows to specify a path
       interpreted by SleuthKit specific VFS classes. The path can be
       specified as either a location string or an inode number. Note
       that looking up an inode number in SleuthKit can be faster than
       looking up a location string.

    Args:
      inode: optional SleuthKit inode string.
      location: optional SleuthKit location string.
      parent: optional parent path specification (instance of PathSpec),
              default is None.
      kwargs: a dictionary of keyword arguments dependending on the path
              specification

    Raises:
      ValueError: when inode and location, or parent are not set.
    """
    if (not inode and not location) or not parent:
      raise ValueError(u'Missing inode and location or parent value.')

    super(TSKPathSpec, self).__init__(parent=parent, **kwargs)
    self.inode = inode
    self.location = location

  @property
  def comparable(self):
    """Comparable representation of the path specification."""
    sub_comparable_string = u''
    if self.inode is not None:
      sub_comparable_string += u'inode: {0:d}'.format(self.inode)
    if self.location is not None:
      sub_comparable_string = u'location: {0:s}\n'.format(self.location)

    return self._GetComparable(sub_comparable_string)


# Register the path specification with the factory.
factory.Factory.RegisterPathSpec(TSKPathSpec)