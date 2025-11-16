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
# @file        express.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-10-26     xqyjlj       initial version
#


import ast
import copy
import re
from collections import defaultdict
from enum import Enum
from typing import Any

from loguru import logger
from simpleeval import AttributeDoesNotExist, NameNotDefined, simple_eval


class Express:
    class Status(Enum):
        ALWAYS_TRUE = 0
        ALWAYS_FALSE = 1
        UNKNOWN = 2

    @staticmethod
    def __eval(
        expression: str, values: dict, replaces: dict[str, str], default: Any
    ) -> Any:
        rtn = default
        expression = Express.convert_expr(expression)
        for key, value in replaces.items():
            expression = expression.replace(key, value)
        try:
            expression = expression.replace(":", ".")
            rtn = simple_eval(expression, names=values)
        except NameNotDefined as e:
            logger.warning(f"{e}, with {expression!r}")
        except AttributeDoesNotExist as e:
            logger.warning(f"{e}, with {expression!r}")
        except Exception as e:
            logger.warning(f"{e}, with {expression!r}")
        return rtn

    @staticmethod
    @logger.catch(default=-1.0)
    def __float_expr(expression: str, values: dict, replaces: dict) -> float:
        return float(Express.__eval(expression, values, replaces, -1.0))

    @staticmethod
    def float_expr(expression: str, values: dict, replaces: dict = {}) -> float:
        return Express.__float_expr(expression, values, replaces)

    @staticmethod
    @logger.catch(default=-1)
    def __int_expr(expression: str, values: dict, replaces: dict) -> int:
        return int(Express.__eval(expression, values, replaces, -1))

    @staticmethod
    def int_expr(expression: str, values: dict, replaces: dict = {}) -> int:
        return Express.__int_expr(expression, values, replaces)

    @staticmethod
    @logger.catch(default=False)
    def __bool_expr(expression: str, values: dict[str, bool], replaces: dict) -> bool:
        return bool(Express.__eval(expression, values, replaces, False))

    @staticmethod
    def bool_expr(expression: str, values: dict, replaces: dict = {}) -> bool:
        return Express.__bool_expr(expression, values, replaces)

    @staticmethod
    def convert_expr(expression: str) -> str:
        expression = expression.replace("!", " not ")
        expression = expression.replace("|", " or ")
        expression = expression.replace("&", " and ")
        expression = expression.replace("=", " == ")
        expression = expression.replace("$", "_xx36xx_")
        expression = expression.replace(":", "_xx58xx_")
        return expression.strip()

    @staticmethod
    def restore_expr(expression: str) -> str:
        expression = expression.replace("_xx36xx_", "$")
        expression = expression.replace("_xx58xx_", ":")
        return expression

    @staticmethod
    def convert_expr_op(expression: str) -> str:
        expression = expression.replace("!", " not ")
        expression = expression.replace("|", " or ")
        expression = expression.replace("&", " and ")
        expression = re.sub(r"(?<![=])=(?![=])", " == ", expression)
        expression = expression.replace("  ", " ")
        return expression.strip()

    @staticmethod
    def variables(expression: str) -> dict[str, list[str]]:
        expression = Express.convert_expr(expression)

        class Visitor(ast.NodeVisitor):
            def __init__(self):
                self.parent = {}
                self.vars = defaultdict(set)

            def set_parent(self, tree):
                for node in ast.walk(tree):
                    for child in ast.iter_child_nodes(node):
                        self.parent[child] = node

            def get_var_name(self, node):
                if isinstance(node, ast.Name):
                    return node.id
                elif isinstance(node, ast.Attribute):
                    parts = []
                    cur = node
                    while isinstance(cur, ast.Attribute):
                        parts.append(cur.attr)
                        cur = cur.value
                    if isinstance(cur, ast.Name):
                        parts.append(cur.id)
                        return ".".join(reversed(parts))
                return None

            def mark_context(self, node):
                p = self.parent.get(node)
                var_name = self.get_var_name(node)
                if not var_name:
                    return

                # 比较 a == b 左右
                if isinstance(p, ast.Compare):
                    if node is p.left:
                        self.vars[var_name].add("lhs")
                    elif node in p.comparators:
                        self.vars[var_name].add("rhs")

                # 布尔逻辑：and/or/not, if, while
                if isinstance(p, (ast.BoolOp, ast.UnaryOp)):
                    self.vars[var_name].add("bool")
                if isinstance(p, ast.If) and p.test is node:
                    self.vars[var_name].add("bool")
                if isinstance(p, ast.While) and p.test is node:
                    self.vars[var_name].add("bool")

            def visit_Name(self, node):
                self.mark_context(node)
                self.generic_visit(node)

            def visit_Attribute(self, node):
                self.mark_context(node)
                self.generic_visit(node)

        # ---- Parse AST ----
        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError as e:
            raise ValueError(f"Invalid expression syntax: {e}")

        v = Visitor()
        v.set_parent(tree)
        v.visit(tree)

        root = tree.body

        # 单变量表达式
        if isinstance(root, (ast.Name, ast.Attribute)):
            var = v.get_var_name(root)
            if var:
                v.vars[var].add("bool")

        # ---- 反向恢复变量名 ----
        restored = {
            Express.restore_expr(name): sorted(ctx) for name, ctx in v.vars.items()
        }

        return restored

    @staticmethod
    def is_prebuilt_variable(symbol: str) -> bool:
        if symbol.endswith("_Exist"):
            return True

        if symbol.isupper():
            if symbol.startswith("STM32"):
                return True
            if symbol.startswith("DIE"):
                if bool(re.compile(r"^[A-Z][A-Z0-9]*\d$").match(symbol)):
                    return True
            if symbol.startswith("LQFP"):
                return True

        if symbol in ["false", "true"]:
            return True

        return False

    @staticmethod
    def get_expression_status(expression: str, context: dict) -> Status:
        result = Express.Status.ALWAYS_FALSE
        variables = Express.variables(expression).keys()
        context = copy.deepcopy(context)
        for variable in variables:
            if not Express.is_prebuilt_variable(variable):
                result = Express.Status.UNKNOWN
            else:
                if variable not in context:
                    context[variable] = False

        if result == Express.Status.UNKNOWN:
            return Express.Status.UNKNOWN
        elif Express.bool_expr(expression, context):
            return Express.Status.ALWAYS_TRUE
        else:
            return Express.Status.ALWAYS_FALSE

    @staticmethod
    def replace_word_keep_case(text: str, old: str, new: str) -> str:
        def repl(match: re.Match):
            word: str = match.group(0)
            if word.isupper():
                return new.upper()
            elif word.islower():
                return new.lower()
            elif word[0].isupper():
                return new.capitalize()
            else:
                return "".join(
                    n.upper() if o.isupper() else n.lower()
                    for o, n in zip(word, new.ljust(len(word)))
                )

        return re.sub(re.escape(old), repl, text, flags=re.IGNORECASE)

    @staticmethod
    def camel_to_snake(string: str) -> str:
        """
        Convert a camelCase or PascalCase string to snake_case.

        This method transforms a given string from camelCase or PascalCase format
        to snake_case format by inserting underscores between words and
        converting all characters to lowercase.

        Args:
            name (str): The input string in camelCase or PascalCase format.

        Returns:
            str: The converted string in snake_case format.

        Example:
            "camelCase" becomes "camel_case"
            "PascalCase" becomes "pascal_case"
            "ABCTest" becomes "abc_test"
        """
        # Add an underscore between consecutive uppercase letters followed by a lowercase letter
        string = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", string)
        # Add an underscore between a lowercase/digit and an uppercase letter
        string = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", string)
        return string.lower()

    @staticmethod
    def find_common_prefix(strings: list[str]) -> str:
        """查找多个字符串的公共前缀"""
        if not strings:
            return ""

        common_prefix = ""
        min_len = min(len(s) for s in strings)

        for i in range(min_len):
            char = strings[0][i]
            if all(s[i] == char for s in strings):
                common_prefix += char
            else:
                break

        if common_prefix:
            underscore_index = common_prefix.rfind("_")
            if underscore_index > 0:
                common_prefix = common_prefix[: underscore_index + 1]

        return common_prefix
