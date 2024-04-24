#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2022-2024 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        helper_keil.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-04-23     xqyjlj       initial version
#

import os
import xml.etree.ElementTree as etree


def xml_indent(elem: etree.Element, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            xml_indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def get_filetype(file: str):
    file_type = 5

    if file.endswith('.cpp') or file.endswith('.cxx'):
        file_type = 8

    if file.endswith('.c') or file.endswith('.C'):
        file_type = 1

    # assemble file type
    if file.endswith('.s') or file.endswith('.S'):
        file_type = 2

    # header type
    if file.endswith('.h'):
        file_type = 5

    if file.endswith('.lib'):
        file_type = 4

    if file.endswith('.o'):
        file_type = 3

    return file_type


def add_group(parent: etree.Element, name: str, files: list, prefix=""):
    # don't add an empty group
    if len(files) == 0:
        return

    existing_files_name = []
    group = None

    for tmp_group in parent.findall('Group'):
        group_name = tmp_group.find('GroupName').text
        if group_name == name:
            group = tmp_group
            group_files = tmp_group.find('Files')
            if group_files is not None:
                for file in group_files.findall('File'):
                    file_name = file.find('FileName').text
                    # file_path = file.find('FilePath').text
                    existing_files_name.append(file_name)
            break

    if group is None:
        group = etree.SubElement(parent, 'Group')
        group_name = etree.SubElement(group, 'GroupName')
        group_name.text = name
        group_files = etree.SubElement(group, 'Files')

    for f in files:
        name = os.path.basename(f)
        if name not in existing_files_name:
            group_file = etree.SubElement(group_files, 'File')
            group_file_name = etree.SubElement(group_file, 'FileName')

            group_file_name.text = name
            group_file_type = etree.SubElement(group_file, 'FileType')
            group_file_type.text = str(get_filetype(name))
            group_file_path = etree.SubElement(group_file, 'FilePath')
            group_file_path.text = f"{prefix}{f}".replace('/', '\\')
