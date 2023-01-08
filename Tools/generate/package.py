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
# Copyright (C) 2022-2023 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        package.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2023-01-08     xqyjlj       initial version
#

import yaml
import os
from package import *

dir_artifact = os.path.dirname(__file__) + "/artifact"
file_artifact = dir_artifact + "/artifact.xaml"
file_config = os.path.abspath(os.path.dirname(__file__) + "/config/package.yml")
packages = ["LQFP", "LFBGA"]

if not os.path.exists(dir_artifact):
    os.makedirs(dir_artifact)


def main():
    string = ""
    if not os.path.exists(file_config):
        raise OSError("the file: {file} is not exists.".format(file=file_config))
    with open(file_config, "r") as fp:
        string = fp.read()
    config = yaml.load(string, Loader=yaml.FullLoader)
    for name, item in config.items():
        if item["type"] in packages:
            action = item["type"].lower() + ".generate_" + item["type"].lower()
            data = eval(action)(name, item)
            with open(file_artifact, "w") as fp:
                fp.write(data)
        else:
            raise ValueError("please use correct type")


if __name__ == "__main__":
    main()
