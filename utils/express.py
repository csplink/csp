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
# @file        express.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-11-21     xqyjlj       initial version
#

from typing import Any

from loguru import logger
from simpleeval import simple_eval, NameNotDefined, AttributeDoesNotExist


class Express:
    @staticmethod
    def __eval(expression: str, values: dict, default: Any) -> Any:
        rtn = default
        try:
            expression = expression.replace(":", ".")
            rtn = simple_eval(expression, names=values)
        except NameNotDefined:
            pass
        except AttributeDoesNotExist:
            pass
        except Exception as e:
            logger.warning(f"{e}, with {expression!r}")
        return rtn

    @staticmethod
    @logger.catch(default=-1.0)
    def __floatExpr(expression: str, values: dict) -> float:
        return float(Express.__eval(expression, values, -1.0))

    @staticmethod
    def floatExpr(expression: str, values: dict) -> float:
        # noinspection PyTypeChecker, PyArgumentList
        return Express.__floatExpr(expression, values)

    @staticmethod
    @logger.catch(default=-1)
    def __intExpr(expression: str, values: dict) -> int:
        return int(Express.__eval(expression, values, -1))

    @staticmethod
    def intExpr(expression: str, values: dict) -> int:
        # noinspection PyTypeChecker, PyArgumentList
        return Express.__intExpr(expression, values)

    @staticmethod
    @logger.catch(default=False)
    def __boolExpr(expression: str, values: dict[str, bool]) -> bool:
        return bool(Express.__eval(expression, values, False))

    @staticmethod
    def boolExpr(expression: str, values: dict) -> bool:
        # noinspection PyTypeChecker, PyArgumentList
        return Express.__boolExpr(expression, values)
