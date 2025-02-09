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
# @file        mcu2summary.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-10-16     xqyjlj       initial version
#

# TODO: 1. 支持所有芯片组modules分类
# TODO: 2. 支持所有文档的分组
# TODO: 3. 支持差异更新

import argparse
import os
import re
import sqlite3
import sys
import xml.etree.ElementTree as etree
from pathlib import Path

import yaml


class Mcu2Summary:
    __documents_group = {
        "product_specifications": "datasheets",
        "reference_manuals": "references",
        "errata_sheets": "errata",
    }

    __modules_group = {
        "BDMA": {"group": "System Core"},
        "CORTEX_M0+": {"group": "System Core"},
        "CORTEX_M7": {"group": "System Core"},
        "DMA": {"group": "System Core"},
        "GPIO": {"group": "System Core"},
        "IWDG": {"group": "System Core"},
        "MDMA": {"group": "System Core"},
        "NVIC": {"group": "System Core"},
        "RAMECC": {"group": "System Core"},
        "RCC": {"group": "System Core"},
        "SYS": {"group": "System Core"},
        "WWDG": {"group": "System Core"},
        "ADC": {"group": "Analog"},
        "DAC": {"group": "Analog"},
        "COMP": {"group": "Analog"},
        "OPAMP": {"group": "Analog"},
        "VREFBUF": {"group": "Analog"},
        "HRTIM": {"group": "Timers"},
        "LPTIM": {"group": "Timers"},
        "RTC": {"group": "Timers"},
        "TIM1_8C0": {"group": "Timers"},
        "TIM1_8H7": {"group": "Timers"},
        "TIM6_7H7": {"group": "Timers"},
        "IRTIM": {"group": "Connectivity"},
        "ETH": {"group": "Connectivity"},
        "FDCAN": {"group": "Connectivity"},
        "FMC": {"group": "Connectivity"},
        "I2C": {"group": "Connectivity"},
        "LPUART": {"group": "Connectivity"},
        "MDIOS": {"group": "Connectivity"},
        "QUADSPI": {"group": "Connectivity"},
        "SDMMC": {"group": "Connectivity"},
        "SWPMI": {"group": "Connectivity"},
        "SPI": {"group": "Connectivity"},
        "UART": {"group": "Connectivity"},
        "USART": {"group": "Connectivity"},
        "USB_OTG_FS": {"group": "Connectivity"},
        "USB_OTG_HS": {"group": "Connectivity"},
        "DCMI": {"group": "Multimedia"},
        "DMA2D": {"group": "Multimedia"},
        "HDMI_CEC": {"group": "Multimedia"},
        "I2S": {"group": "Multimedia"},
        "JPEG": {"group": "Multimedia"},
        "LTDC": {"group": "Multimedia"},
        "SAI": {"group": "Multimedia"},
        "SPDIFRX": {"group": "Multimedia"},
        "CRYP": {"group": "Security"},
        "HASH": {"group": "Security"},
        "RNG": {"group": "Security"},
        "CRC": {"group": "Computing"},
        "DFSDM": {"group": "Computing"},
        "DEBUG": {"group": "Debug"},
        "PWR": {"group": "Power"},
    }

    def __sortByPositionKey(self, s):
        s = s[1]["position"]
        if isinstance(s, str):
            letter = s[0]
            number = int(s[1:])
            return letter, number
        else:
            return int(s)

    def __getPins(self, pinNodes: list[etree.Element], ns: dict) -> dict:
        pins = {}
        segs = []
        typeMap = {
            "I/O": "I/O",
            "Power": "power",
            "Reset": "reset",
            "NC": "nc",
            "Boot": "boot",
            "MonoIO": "monoIO",
        }
        for pinNode in pinNodes:
            pinName = pinNode.attrib["Name"]
            position: str = pinNode.attrib["Position"]
            if position.isdecimal():
                position: int = int(position)
            type_ = typeMap.get(pinNode.attrib["Type"], pinNode.attrib["Type"])
            signalNodes = pinNode.findall("ns:Signal", ns)
            signals = []
            modes = []
            for signalNode in signalNodes:
                signalName = signalNode.attrib["Name"]
                ioModes = signalNode.attrib.get("IOModes", None)
                if ioModes is not None:
                    ioModes = ioModes.split(",")
                    for mode in ioModes:
                        modes.append(f"{signalName}:{mode}")
                else:
                    signals.append(signalName.replace("_", ":", 1))
            pinItem = {"position": position, "type": type_}
            if len(signals) > 0:
                pinItem["signals"] = signals
            if len(modes) > 0:
                pinItem["modes"] = modes
            if pinName in pins:
                if isinstance(pins[pinName], dict):
                    segs.append(pinName)
                    pins[pinName] = [pins[pinName]]
                # noinspection PyUnresolvedReferences
                pins[pinName].append(pinItem)
            else:
                pins[pinName] = pinItem
        for seg in segs:
            # noinspection PyUnresolvedReferences
            ps = pins.pop(seg)
            num = len(ps)
            for i in range(num):
                pins[f"{seg}-{i + 1}"] = ps[i]
        # noinspection PyUnresolvedReferences
        _pins = sorted(pins.items(), key=self.__sortByPositionKey, reverse=False)
        pins = {k: v for k, v in _pins}
        return pins

    def __getModules(self, ipNodes: list[etree.Element], ns: dict) -> dict:
        ips = {}
        for ipNode in ipNodes:
            name = ipNode.attrib["Name"]
            instanceName = ipNode.attrib["InstanceName"]
            group = "Misc"
            if name in self.__modules_group:
                group = self.__modules_group[name]["group"]
            else:
                pass
                # print(name, instanceName)
            if group not in ips:
                ips[group] = {}
            ips[group][instanceName] = {
                "description": {"en": "", "zh_CN": None},
            }
        return ips

    def __getDocs(self, name: str, cursor: sqlite3.Connection) -> dict:
        cpnObj = cursor.execute(f"SELECT * FROM cpn WHERE refname = '{name}'")
        cpn = cpnObj.fetchall()[0]
        cpnId = cpn[0]
        rpnHasCpnObj = cursor.execute(
            f"SELECT * FROM rpn_has_cpn WHERE cpn_id = '{cpnId}'"
        )
        rpnHasCpn = rpnHasCpnObj.fetchall()[0]
        rpnId = rpnHasCpn[0]
        rpnHasResourceObj = cursor.execute(
            f"SELECT * FROM rpn_has_resource WHERE rpn_id = '{rpnId}'"
        )
        rpnHasResources = rpnHasResourceObj.fetchall()
        resources = {}
        for rpnHasResource in rpnHasResources:
            subcategory = rpnHasResource[2]
            resourceObj = cursor.execute(
                f"SELECT * FROM resource WHERE id = '{rpnHasResource[1]}'"
            )
            resource = resourceObj.fetchall()[0]
            url = resource[1]
            title = resource[2]
            type_ = resource[4]
            description = resource[5]
            size = resource[6]
            version = resource[7]
            subcategoryObj = cursor.execute(
                f"SELECT * FROM subcategory WHERE id = '{subcategory}'"
            )
            subcategory = subcategoryObj.fetchall()[0]
            subcategoryRef = subcategory[4]
            subcategoryName = self.__documents_group.get(subcategoryRef, subcategoryRef)
            if subcategoryName not in resources:
                resources[subcategoryName] = {}
            resources[subcategoryName][title] = {
                "url": {"en": url, "zh_CN": None},
                "type": type_,
                "description": {"en": description, "zh_CN": None},
                "size": size,
                "version": version,
            }
        return resources

    def __getNames(self, name: str, cursor: sqlite3.Connection) -> dict[str, list[str]]:
        rtn = {}
        names = []
        pattern = r"\(.*?\)"
        match = re.search(pattern, name)
        if match is not None:
            match = match.group(0)
            match = match.strip("()")
            if "-" in match:
                startChar, endChar = match.split("-")
                startCode = ord(startChar)
                endCode = ord(endChar)
                codes = [chr(code) for code in range(startCode, endCode + 1)]
                for code in codes:
                    names.append(re.sub(pattern, code, name))
            else:
                names.append(name)
        else:
            names.append(name)

        for name in names:
            cpnObj = cursor.execute(f"SELECT * FROM cpn WHERE refname = '{name}'")
            cpns = cpnObj.fetchall()
            if len(cpns) > 0:
                if name not in rtn:
                    rtn[name] = []
                for cpn in cpns:
                    rtn[name].append(cpn[1])
        return rtn

    def __getUrl(self, name: str, cursor: sqlite3.Connection) -> str:
        mcuObj = cursor.execute(
            f"SELECT URL, refname FROM mcu WHERE refname = '{name}'"
        )
        mcus = mcuObj.fetchall()
        if len(mcus) == 0:
            return ""
        mcu = mcus[0]
        return mcu[0]

    def __getIntroduction(self, name: str, cursor: sqlite3.Connection) -> str:
        mcuObj = cursor.execute(
            f"SELECT description, refname FROM mcu WHERE refname = '{name}'"
        )
        mcus = mcuObj.fetchall()
        if len(mcus) == 0:
            return ""
        mcu = mcus[0]
        return mcu[0]

    def converter(self, path: str, crdbPath: str, cfdbPath: str) -> dict:
        rtn = {}
        crdbCursor = sqlite3.connect(crdbPath)
        cfdbCursor = sqlite3.connect(cfdbPath)

        tree = etree.parse(path)
        root = tree.getroot()
        namespace = {"ns": root.tag.split("}")[0][1:] if "}" in root.tag else ""}
        refName = root.attrib["RefName"]
        family = root.attrib["Family"]
        clockTree = root.attrib["ClockTree"]
        hasPowerPad = root.attrib["HasPowerPad"]
        hasPowerPad = True if hasPowerPad == "true" else False
        package = root.attrib["Package"]
        pinNodes = root.findall("ns:Pin", namespace)
        pins = self.__getPins(pinNodes, namespace)
        ipNodes = root.findall("ns:IP", namespace)
        modules = self.__getModules(ipNodes, namespace)
        names = self.__getNames(refName, cfdbCursor)
        for namex, ns in names.items():
            url = self.__getUrl(namex, crdbCursor)
            introduction = self.__getIntroduction(namex, crdbCursor)
            documents = self.__getDocs(namex, cfdbCursor)
            for n in ns:
                rtn[n] = {
                    "name": n,
                    "clockTree": clockTree,
                    "vendor": "STMicroelectronics",
                    "vendorUrl": {
                        "en": "https://www.st.com.com",
                        "zh_CN": "https://www.st.com.cn",
                    },
                    "documents": documents,
                    "hals": [f"csp_hal_{family.lower()}"],
                    "hasPowerPad": hasPowerPad,
                    "illustrate": {"en": "", "zh_CN": None},
                    "introduction": {"en": introduction, "zh_CN": None},
                    "modules": modules,
                    "package": package,
                    "url": {"en": url, "zh_CN": None},
                    "builder": {
                        "XMake": {"v2.8.1": ["arm-none-eabi"]},
                        "CMake": {"v3.7": ["arm-none-eabi"]},
                        "MDK-Arm": {"v5.27": ["armcc", "armclang"]},
                    },
                    "linker": {
                        "defaultHeapSize": "0x200",
                        "defaultStackSize": "0x400",
                    },
                    "pins": pins,
                }
        cfdbCursor.close()
        crdbCursor.close()
        return rtn

    def generate(self, src: str, dest: str, crdbPath: str, cfdbPath: str):
        mcus = self.converter(src, crdbPath, cfdbPath)
        for name, mcu in mcus.items():
            print(
                f"find {name} mcu, {len(mcu['pins'])} pin! write to {Path(dest).absolute()}/{name.lower()}.yml"
            )
            data = yaml.dump(mcu, allow_unicode=True, sort_keys=False)
            with open(
                f"{os.path.join(dest, f'{name.lower()}.yml')}", "w", encoding="utf-8"
            ) as f:
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
    crdb = args.crdb
    cfdb = args.cfdb

    if not os.path.isfile(file):
        print(f"the file {file!r} is not a file")
        sys.exit(1)

    if not os.path.isfile(crdb):
        print(f"the file {crdb!r} is not a file")
        sys.exit(1)

    if not os.path.isfile(cfdb):
        print(f"the file {cfdb!r} is not a file")
        sys.exit(1)

    if not os.path.isdir(output):
        print(f"the dir {output!r} is not a dir")
        sys.exit(1)

    Mcu2Summary().generate(file, output, crdb, cfdb)


def __createParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="generate csp summary from stm32cubemx mcu xml file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("-f", "--file", required=True, help="stm32cubemx mcu xml file")
    parser.add_argument("-o", "--output", required=True, help="output dir")
    parser.add_argument("--crdb", required=True, help="stm32cubemx crdb.db file")
    parser.add_argument(
        "--cfdb", required=True, help="stm32cubemx cube-finder-db.db file"
    )
    return parser


if __name__ == "__main__":
    __main()
