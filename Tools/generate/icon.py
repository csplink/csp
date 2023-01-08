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
# @file        icon.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2023-01-08     xqyjlj       initial version
#

import os
import pathlib

template_icon_data = """
        public static BitmapImage {name} {{
            get => Instance.{name};
        }}
"""

template_icon_instance_data = "        internal readonly BitmapImage {name} = new(new Uri(@\"pack://application:,,,/CSP.Resources;component/Icon/{name}.png\"));\n"

template_icon_instance = """using System;
using System.Windows.Media.Imaging;

namespace CSP.Resources
{{
    internal class IconInstance
    {{
{data}    }}
}}"""

template_icon = """using System.Windows.Media.Imaging;

namespace CSP.Resources
{{
    public static class Icon
    {{
        private static readonly IconInstance Instance = new();
{data}    }}
}}"""

dir_resources = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "/Resources/CSP.Resources"
dir_resources_icon = dir_resources + "/Icon"
path_resources_icon = dir_resources + "/Icon.cs"
path_resources_icon_instance = dir_resources + "/IconInstance.cs"


def main():
    data_icon_instance = ""
    data_icon = ""
    p = pathlib.Path(dir_resources_icon)
    ret = p.glob("*.png")
    for item in ret:
        name = str(item.name).replace(".png", "")
        data_icon_instance += template_icon_instance_data.format(name=name)
        data_icon += template_icon_data.format(name=name)
    icon_instance = template_icon_instance.format(data=data_icon_instance)
    icon = template_icon.format(data=data_icon)

    with open(path_resources_icon_instance, "w", encoding="utf-8") as fp:
        fp.write(icon_instance)

    with open(path_resources_icon, "w", encoding="utf-8") as fp:
        fp.write(icon)


if __name__ == "__main__":
    main()
