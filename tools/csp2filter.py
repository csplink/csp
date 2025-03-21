#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the GNU General Public License v. 3 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/gpl-3.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2024-2024 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        csp2filter.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-12-28     xqyjlj       initial version
#

import argparse
import os
import sys
import time

import jinja2
import yaml


class Csp2Filter:
    @staticmethod
    def generate(project: dict, output: str, modules: list[str]):
        __template = """#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the GNU General Public License v. 3 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/gpl-3.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) {{ year }}-{{ year }} csplink<https://csplink.top/>
#
# @author      csplink
# @file        {{ module }}.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# {{ date }}     csplink      initial version
#

import csp_project_helper
{# #}
{# #}
{%- for name, value in configs.items() %}
def {{ name }}(project: dict, default: {{ value.type }} | None = None) -> {{ value.type }}:
    return csp_project_helper.get(project, '{{ value.path }}', default)
{# #}
{# #}
{%- endfor %}
"""
        if len(modules) == 1 and modules[0] == "all":
            modules = project.get("modules", [])

        for module in modules:
            module_cfg = project.get("configs", {}).get(module, {})
            configs = {}

            for key, value in module_cfg.items():
                key: str
                if not isinstance(value, dict):
                    configs[key.split(".")[-1]] = {
                        "path": f"configs/{module}/{key}",
                        "type": type(value).__name__,
                    }
            data = {
                "module": module.lower(),
                "date": time.strftime("%Y-%m-%d", time.localtime()),
                "year": time.strftime("%Y", time.localtime()),
                "configs": configs,
            }
            env = jinja2.Environment()
            template = env.from_string(__template)
            context = template.render(data)

            path = f"{output}/{module.lower()}.py".replace("\\", "/")
            print(f"generate {path!r}.")

            with open(path, "w", encoding="utf-8") as f:
                f.write(context)


def __main():
    try:
        parser = __create_parser()
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        print(e)
        sys.exit(1)

    file = args.file
    output = args.output
    modules = args.modules

    if not os.path.isfile(file):
        print(f"the file {file!r} is not a file")
        sys.exit(1)

    if output is None or not os.path.isdir(output):
        output = os.path.dirname(file)

    if not os.path.isdir(output):
        os.makedirs(output)

    with open(file, "r", encoding="utf-8") as f:
        project = yaml.load(f.read(), Loader=yaml.FullLoader)

    Csp2Filter.generate(project, output, modules)


def __create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="generate jinja2 template filter from csp project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("-f", "--file", required=True, help="csp project file")
    parser.add_argument("-o", "--output", required=False, help="output dir")
    parser.add_argument(
        "-m",
        "--modules",
        required=False,
        nargs="+",
        default=["all"],
        help="dump modules",
    )
    return parser


if __name__ == "__main__":
    __main()
