#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the Apache License v. 2 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2025-2025 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        tc_tools_cmx_ip.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-10-31     xqyjlj       initial version
#

import os
import unittest

from actions import action_tools_cmx_ip
from loguru import logger
from utils.io import IO_UTILS
from utils.sys import SYS_UTILS

ip_folder = os.path.join(SYS_UTILS.exe_folder(), "tests", "resources", "cmx", "ip")
mcu_file_path = os.path.join(
    SYS_UTILS.exe_folder(),
    "tests",
    "resources",
    "cmx",
    "mcu",
    "STM32F103Z(C-D-E)Tx.xml",
)
ip_file_list = [
    "CAN-bxcan1_v1_1_F1_Cube_Modes.xml",
    "CRC-integtest1_v1_0_Modes.xml",
    # "DAC-dacif_v1_1F1_Cube_Modes.xml",
    # "DMA-STM32F103G_dma_v1_0_Modes.xml",
    # "FSMC-fsmc7_v1_0_Modes.xml",
    "GPIO-STM32F103xC_gpio_v1_0_Modes.xml",
    # "I2C-i2c1_v1_5_Cube_Modes.xml",
    # "I2S-spi2s1_v1_0_Cube_Modes.xml",
    "IWDG-iwdg1_v1_1_Modes.xml",
    # "NVIC-STM32F103G_Modes.xml",
    # "RCC-STM32F102_rcc_v1_0_Modes.xml",
    # "RTC-rtc1_v1_1_Cube_Modes.xml",
    "SDIO-sdmmc_v1_2_Cube_Modes.xml",
    # "SPI-spi2s1_v1_0_Cube_Modes.xml",
    "SYS-STM32F10x_sys_v1_0_Modes.xml",
    # "TIM1_8F1-gptimer2_v1_x_Cube_Modes.xml",
    # "TIM6_7F1-gptimer2_v1_x_Cube_Modes.xml",
    "UART-sci2_v1_1_Cube_Modes.xml",
    "USART-sci2_v1_1_Cube_Modes.xml",
    # "USB-usb1_v1_1_Cube_Modes.xml",
    "WWDG-wwdg1_v1_0_Modes.xml",
]


class TcToolsCmxIpFunctional(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_system(self):
        for fname in ip_file_list:
            fpath = os.path.join(ip_folder, fname)
            base, _ = os.path.splitext(fpath)
            output = f"{base}.yml"
            target = f"{base}.yml.target"
            logger.info(f"Testing {fname}...")
            action_tools_cmx_ip(fpath, mcu_file_path, output, "")
            output_yml = IO_UTILS.read_yaml(output)
            target_yml = IO_UTILS.read_yaml(target)
            self.assertDictEqual(output_yml, target_yml)

    def tearDown(self):
        pass
