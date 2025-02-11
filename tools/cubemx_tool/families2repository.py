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
# Copyright (C) 2022-2024 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        families2repository.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-10-14     xqyjlj       initial version
#

# TODO: 1. 支持 cube-finder-db.db, crdb.db 的导入
# TODO: 2. 支持特定名称MCU导出
# TODO: 3. 支持差异更新

import argparse
import os
import sys
import xml.etree.ElementTree as etree
from pathlib import Path

import yaml


class Families2Repository:

    def converter(self, path: str) -> dict[str, dict]:
        items = {}
        tree = etree.parse(path)
        root = tree.getroot()
        for familyNode in root:
            seriesName = familyNode.attrib["Name"]
            lines = {}
            for subFamilyNode in familyNode:
                lineName = subFamilyNode.attrib["Name"]
                socs = {}
                for mcuNode in subFamilyNode:
                    name = mcuNode.attrib.get("RefName", None)
                    package = mcuNode.attrib.get("PackageName", None)
                    core = mcuNode.findtext("Core")
                    frequency = mcuNode.findtext("Frequency")
                    ram = mcuNode.findtext("Ram")
                    io = mcuNode.findtext("IONb")
                    flash = mcuNode.findtext("Flash")

                    if (
                        name is None
                        or package is None
                        or core is None
                        or frequency is None
                        or ram is None
                        or io is None
                        or flash is None
                    ):
                        continue

                    voltageNode = mcuNode.find("Voltage")
                    if voltageNode is not None:
                        voltageMax = voltageNode.attrib.get("Max", -1)
                        voltageMin = voltageNode.attrib.get("Min", -1)
                    else:
                        voltageMax = -1
                        voltageMin = -1
                    temperatureNode = mcuNode.find("Temperature")
                    if temperatureNode is not None:
                        temperatureMax = temperatureNode.attrib.get("Max", -1)
                        temperatureMin = temperatureNode.attrib.get("Min", -1)
                    else:
                        temperatureMax = -1
                        temperatureMin = -1
                    currentNode = mcuNode.find("Current")
                    if currentNode is not None:
                        currentLowest = currentNode.attrib.get("Lowest", -1)
                        currentRun = currentNode.attrib.get("Run", -1)
                    else:
                        currentLowest = -1
                        currentRun = -1

                    peripheralNodes = mcuNode.findall("Peripheral")
                    peripherals = {}
                    for peripheralNode in peripheralNodes:
                        _kind = peripheralNode.attrib.get("Type", None)
                        num = peripheralNode.attrib.get("MaxOccurs", 0)
                        peripherals[_kind] = int(num)

                    socs[name] = {
                        "core": core,
                        "package": package,
                        "frequency": int(frequency),
                        "ram": int(ram),
                        "io": int(io),
                        "flash": int(flash),
                        "voltage": {"max": float(voltageMax), "min": float(voltageMin)},
                        "current": {
                            "lowest": float(currentLowest),
                            "run": float(currentRun),
                        },
                        "temperature": {
                            "max": float(temperatureMax),
                            "min": float(temperatureMin),
                        },
                        "peripherals": peripherals,
                    }
                lines[lineName] = socs
            items[seriesName] = lines
        return {"soc": {"STMicroelectronics": items}}

    def generate(self, src: str, dest: str):
        repo = self.converter(src)
        seriesNum = 0
        lineNum = 0
        socNum = 0
        for kind, kindItem in repo.items():
            for vendor, vendorItem in kindItem.items():
                seriesNum += len(vendorItem)
                for series, seriesItem in vendorItem.items():
                    lineNum += len(seriesItem)
                    for line, lineItem in seriesItem.items():
                        socNum += len(lineItem)
        print(f"find {seriesNum} series, {lineNum} line, {socNum} soc!")
        print(f"write to {Path(dest).absolute()}")
        data = yaml.dump(repo)
        with open(dest, "w") as f:
            f.write(data)


def __help():
    pass


def __main():
    try:
        parser = __createParser()
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        print(e)
        sys.exit(1)

    file = args.file
    output = args.output

    if not os.path.isfile(file):
        print(f"the file {file!r} is not a file")
        sys.exit(1)

    if not os.path.isdir(output):
        print(f"the dir {output!r} is not a dir")
        sys.exit(1)

    dest = os.path.join(output, "repository.yaml")

    Families2Repository().generate(file, dest)


def __createParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="generate csp repository from stm32cubemx families.xml file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("-f", "--file", required=True, help="stm32cubemx mcu xml file")
    parser.add_argument("-o", "--output", required=True, help="output dir")
    return parser


if __name__ == "__main__":
    __main()
