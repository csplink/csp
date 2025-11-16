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
# @file        tc_functional.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-01     xqyjlj       initial version
#

import os
import unittest

from loguru import logger
from ruamel.yaml import YAML
from utils.express import Express
from utils.io import IO_UTILS
from utils.sys import SYS_UTILS

express_list = [
    "SYS_TIM1",
    "SYS_TIM2",
    "SYS_TIM3",
    "SYS_TIM4",
    "SYS_TIM5",
    "SYS_TIM6",
    "SYS_TIM7",
    "SYS_TIM8",
    "SYS_TIM9",
    "SYS_TIM10",
    "SYS_TIM11",
    "SYS_TIM12",
    "SYS_TIM13",
    "SYS_TIM14",
    "SYS_TIM15",
    "SYS_TIM16",
    "SYS_TIM17",
    "SYS_TIM18",
    "SYS_TIM19",
    "SYS_TIM20",
    "SYS_TIM21",
    "SYS_TIM22",
    "SYS_TIM23",
    "SYS_RTC",
    "!TIM1",
    "!TIM2",
    "!TIM3",
    "!TIM4",
    "!TIM5",
    "!TIM6",
    "!TIM7",
    "!TIM8",
    "!TIM9",
    "!TIM10",
    "!TIM11",
    "!TIM12",
    "!TIM13",
    "!TIM14",
    "!TIM15",
    "!TIM16",
    "!TIM17",
    "!TIM18",
    "!TIM19",
    "!TIM20",
    "!TIM21",
    "!TIM22",
    "!TIM23",
    "VirtualMode = IrDA",
    "VirtualMode = IrDA",
    "$IpInstance_LIN",
    "VirtualMode = IrDA & WordLength=WORDLENGTH_8B",
    "VirtualMode = IrDA & WordLength=WORDLENGTH_9B",
    "WordLength=WORDLENGTH_8B",
    "WordLength=WORDLENGTH_9B",
    "StopBits=UART_STOPBITS_1",
    "StopBits=UART_STOPBITS_2",
    "VirtualMode = IrDA & $IpInstance_PARITY_NONE",
    "VirtualMode = IrDA & $IpInstance_PARITY_EVEN",
    "VirtualMode = IrDA & $IpInstance_PARITY_ODD",
    "$IpInstance_PARITY_NONE",
    "$IpInstance_PARITY_EVEN",
    "$IpInstance_PARITY_ODD",
    "VirtualMode = IrDA & S_$IpInstance_TX_RX",
    "VirtualMode = IrDA & S_$IpInstance_TX",
    "VirtualMode = IrDA & S_$IpInstance_RX",
    "S_$IpInstance_TX_RX",
    "S_$IpInstance_TX",
    "S_$IpInstance_RX",
    "(VirtualMode = Lin) | (VirtualMode = IrDA)",
    "IrDAMode = IRDA_POWERMODE_NORMAL",
    "DIE436|DIE427|DIE437|DIE416|STM32F1",
    "WakeUpMethode = UART_WAKEUPMETHOD_ADDRESSMARK",
    "VirtualMode = VM_SYNC",
    "VirtualMode = VM_IRDA",
    "VirtualMode = VM_SMARTCARD",
    "$IpInstance_LIN",
    "VirtualMode = VM_SYNC & WordLength=WORDLENGTH_8B",
    "VirtualMode = VM_SYNC & WordLength=WORDLENGTH_9B",
    "VirtualMode = VM_IRDA & WordLength=WORDLENGTH_8B",
    "VirtualMode = VM_IRDA & WordLength=WORDLENGTH_9B",
    "VirtualMode = VM_SMARTCARD & WordLength=WORDLENGTH_9B",
    "WordLength=WORDLENGTH_8B",
    "WordLength=WORDLENGTH_9B",
    "VirtualMode = VM_SYNC",
    "$IpInstance_Asynchronous & (STM32F0 | STM32F3 | STM32L4) ",
    "$IpInstance_Asynchronous & STM32L0",
    "VirtualMode = VM_SMARTCARD",
    "(VirtualMode = VM_SYNC) & StopBits=STOPBITS_2",
    "(VirtualMode = VM_SYNC) & StopBits=STOPBITS_1",
    "VirtualMode = VM_SYNC & StopBits=STOPBITS_1_5",
    "VirtualMode = VM_SYNC & StopBits=STOPBITS_0_5",
    "$IpInstance_Asynchronous & StopBits=STOPBITS_1",
    "$IpInstance_Asynchronous & StopBits=STOPBITS_2",
    "$IpInstance_Asynchronous & StopBits=STOPBITS_1_5",
    "VirtualMode = VM_SMARTCARD & StopBits=STOPBITS_1_5",
    "VirtualMode = VM_SMARTCARD & StopBits=STOPBITS_0_5",
    "StopBits=STOPBITS_1",
    "StopBits=STOPBITS_2",
    "VirtualMode = VM_SMARTCARD",
    "$IpInstance_PARITY_NONE & VirtualMode=VM_SYNC",
    "$IpInstance_PARITY_ODD & VirtualMode=VM_SYNC",
    "$IpInstance_PARITY_EVEN & VirtualMode=VM_SYNC",
    "$IpInstance_PARITY_NONE & VirtualMode=VM_IRDA",
    "$IpInstance_PARITY_EVEN & VirtualMode=VM_IRDA",
    "$IpInstance_PARITY_ODD & VirtualMode=VM_IRDA",
    "(Parity = PARITY_EVEN) & VirtualMode=VM_SMARTCARD",
    "(Parity = PARITY_ODD) & VirtualMode=VM_SMARTCARD",
    "$IpInstance_PARITY_NONE",
    "$IpInstance_PARITY_EVEN",
    "$IpInstance_PARITY_ODD",
    "S_$IpInstance_TX_RX & VirtualMode=VM_SYNC",
    "S_$IpInstance_TX & VirtualMode=VM_SYNC",
    "S_$IpInstance_RX & VirtualMode=VM_SYNC",
    "S_$IpInstance_TX_RX & VirtualMode=VM_SMARTCARD",
    "S_$IpInstance_TX & VirtualMode=VM_SMARTCARD",
    "S_$IpInstance_RX & VirtualMode=VM_SMARTCARD",
    "S_$IpInstance_TX_RX & VirtualMode=VM_IRDA",
    "S_$IpInstance_TX & VirtualMode=VM_IRDA",
    "S_$IpInstance_RX & VirtualMode=VM_IRDA",
    "S_$IpInstance_TX_RX",
    "S_$IpInstance_TX",
    "S_$IpInstance_RX",
    "$IpInstance_R",
    "$IpInstance_T",
    "$IpInstance_CTS_RTS",
    "((VirtualMode = VM_SYNC) | (VirtualMode = VM_IRDA) | (VirtualMode = VM_SMARTCARD) | $IpInstance_LIN)",
    "VirtualClockMode = VM_SMARTCARD",
    "VirtualMode = VM_SYNC",
    "VirtualClockMode = VM_SMARTCARD",
    "VirtualMode = VM_SYNC",
    "VirtualClockMode = VM_SMARTCARD",
    "VirtualMode = VM_SYNC",
    "(IrDAMode = IRDA_POWERMODE_NORMAL) & (VirtualMode = VM_IRDA)",
    "(VirtualMode=VM_SMARTCARD) & (VirtualClockMode=VM_SMARTCARD)",
    "VirtualMode = VM_SMARTCARD",
    "DIE436|DIE427|DIE437|DIE416|STM32F1",
    "WakeUpMethode = UART_WAKEUPMETHOD_ADDRESSMARK",
    "$IpInstance_Asynchronous",
    "STM32F0|STM32F1|STM32F2|STM32F3|STM32F4|STM32F7|STM32L0|STM32L1|STM32L4|STM32WB",
    "F100_Value_Line &((($Index=1|$Index=2)& USE_ADC1&USE_ADC2)&(ADC1:InjNumberOfConversion=0)&(ADC2:InjNumberOfConversion=0))|((($IpInstance=ADC3|$IpInstance=ADC4)&USE_ADC3&USE_ADC4&(ADC3:InjNumberOfConversion=0)&(ADC4:InjNumberOfConversion=0)))",
]

express_file_path = os.path.join(
    SYS_UTILS.exe_folder(),
    "tests",
    "resources",
    "utils",
    "express.yml",
)


class TcUtilsExpressFunctional(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_variables(self):
        configs = {}
        with open(express_file_path, "r", encoding="utf-8") as f:
            yaml = YAML()
            configs = yaml.load(f)
        for express, context in configs.items():
            logger.trace(f"Testing {express}...")
            rtn = Express.variables(express)
            self.assertEqual(rtn, context["context"])

    def tearDown(self):
        pass
