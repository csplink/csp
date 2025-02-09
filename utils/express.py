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

import ast
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

    @staticmethod
    def variables(expression: str) -> list[str]:
        """
        Extract all variable names from a Python expression string.

        Args:
            expr (str): The Python expression string to analyze

        Returns:
            list: Sorted list of unique variable names in dot-separated format

        Raises:
            ValueError: If the input expression has invalid syntax
        """

        class _VariableCollector(ast.NodeVisitor):
            """
            AST node visitor that collects variable names from:
            - Simple identifiers (Name nodes)
            - Attribute chains (e.g., foo.bar.baz)

            Skips names that are part of longer attribute chains
            """

            def __init__(self, parent_map):
                # Store parent-child relationships to check context
                self.parent_map = parent_map
                # Use set to avoid duplicates
                self.variables = set()

            def visit_Name(self, node):
                """
                Handle simple variable names (e.g., 'x' in 'x == 5')
                Skip names that are part of attribute chains (e.g., 'x' in 'x.y')
                """
                parent = self.parent_map.get(node)
                # Check if this name is part of an attribute chain
                if isinstance(parent, ast.Attribute) and parent.value is node:
                    return  # Skip as it will be handled by visit_Attribute
                # Add standalone variable name
                self.variables.add(node.id)
                self.generic_visit(node)

            def visit_Attribute(self, node):
                """
                Handle dotted attribute chains (e.g., 'a.b.c')
                Converts nested Attribute nodes to dot-separated string
                """
                parent = self.parent_map.get(node)
                # Skip if this attribute is part of a longer chain
                if isinstance(parent, ast.Attribute) and parent.value is node:
                    return

                # Deconstruct the attribute chain
                parts = []
                current = node
                while isinstance(current, ast.Attribute):
                    parts.append(current.attr)  # Collect attribute names
                    current = current.value  # Move to parent node

                # Handle the base variable name
                if isinstance(current, ast.Name):
                    parts.append(current.id)
                    parts.reverse()  # Reverse to get correct order
                    var_name = ".".join(parts)
                    self.variables.add(var_name)

                self.generic_visit(node)

        try:
            # Parse the expression into an Abstract Syntax Tree (AST) using eval mode
            tree = ast.parse(expression, mode="eval")
        except SyntaxError as e:
            raise ValueError(f"Invalid expression syntax: {e}")

        # Build parent-child node relationships to track attribute context
        parent_map = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                parent_map[child] = node
        # Use custom visitor to collect variables from AST
        visitor = _VariableCollector(parent_map)
        visitor.visit(tree)
        return sorted(visitor.variables)
