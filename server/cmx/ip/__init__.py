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
# @file        __init__.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-05     xqyjlj       initial version
#

from .base import Base as CmxIpBase
from .condition import Condition as CmxIpCondition
from .ip import Ip as CmxIp
from .mode1 import Mode1 as CmxIpMode1
from .mode2 import Mode2 as CmxIpMode2
from .mode_logic_operator1 import ModeLogicOperator1 as CmxIpModeLogicOperator1
from .mode_logic_operator2 import ModeLogicOperator2 as CmxIpModeLogicOperator2
from .parameter import Parameter as CmxIpParameter
from .possible_value import PossibleValue as CmxIpPossibleValue
from .ref_mode import RefMode as CmxIpRefMode
from .ref_parameter import RefParameter as CmxIpRefParameter
from .ref_signal import RefSignal as CmxIpRefSignal
from .share import Share as CmxIpShare
from .signal import Signal as CmxIpSignal
from .signal_logical_op import SignalLogicalOp as CmxIpSignalLogicalOp

__all__ = [
    "CmxIpBase",
    "CmxIpCondition",
    "CmxIp",
    "CmxIpMode1",
    "CmxIpMode2",
    "CmxIpModeLogicOperator1",
    "CmxIpModeLogicOperator2",
    "CmxIpParameter",
    "CmxIpPossibleValue",
    "CmxIpRefMode",
    "CmxIpRefParameter",
    "CmxIpRefSignal",
    "CmxIpShare",
    "CmxIpSignal",
    "CmxIpSignalLogicalOp",
]
