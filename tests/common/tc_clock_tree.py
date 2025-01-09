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
# @file        tc_clock_tree.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-12-06     xqyjlj       initial version
#

import unittest
from collections import defaultdict

from common import Repository, SUMMARY, CLOCK_TREE, ClockTreeType


class ClockTreeTest(unittest.TestCase):

    def setUp(self):
        pass

    def detect_all_cycles(self, data: dict[str, ClockTreeType.ElementUnitType], kind: str):
        # build a directed graph
        graph = defaultdict(list)
        for node, details in data.items():
            if kind == 'output':
                # add edges based on 'output'
                for name in details.output:
                    graph[node].append(name)
            else:
                # add edges based on 'input'
                for name in details.input:
                    graph[node].append(name)

        visited = set()  # set to track visited nodes
        recursion_stack = {}  # stack to track nodes in the current DFS path
        all_cycles = []  # list to store all detected cycles

        # helper function for DFS
        def dfs(node_, path):
            if node_ in recursion_stack:  # a cycle is detected
                cycle_start_index = path.index(node_)  # find where the cycle starts
                cycle_path = path[cycle_start_index:]  # extract the cycle path
                all_cycles.append(cycle_path + [node_])  # add the cycle to the result list
                return

            if node_ in visited:  # skip already visited nodes
                return

            # mark the node as visited and add it to the recursion stack
            visited.add(node_)
            recursion_stack[node_] = True
            path.append(node_)

            # explore all neighbors
            for neighbor in graph[node_]:
                dfs(neighbor, path)

            # remove the node from the recursion stack and the current path
            recursion_stack.pop(node_, None)
            path.pop()

        # start DFS from each unvisited node
        for node in data.keys():
            if node not in visited:
                dfs(node, [])

        return all_cycles

    def test_getClockTree(self):
        repository = Repository()
        socs = repository.repository().allSoc()
        dones = []
        for soc in socs:
            summary = SUMMARY.getSummary(soc.vendor, soc.name)
            if summary.clockTree in dones:
                continue
            dones.append(summary.clockTree)
            clockTree = CLOCK_TREE.getClockTree(soc.vendor, summary.clockTree)

            for _, elem in clockTree.elements.items():
                for name in elem.input:
                    self.assertTrue(name in clockTree.elements, msg=f'the {name!r} is not exits!')
                for name in elem.output:
                    self.assertTrue(name in clockTree.elements, msg=f'the {name!r} is not exits!')

            inputCycles = self.detect_all_cycles(clockTree.elements, 'input')
            if inputCycles:
                print("input node cycles detected!")
                for i, cycle in enumerate(inputCycles, 1):
                    print(f"    cycle {i}: {' -> '.join(cycle)}")
            outputCycles = self.detect_all_cycles(clockTree.elements, 'output')
            if outputCycles:
                print("output node cycles detected!")
                for i, cycle in enumerate(outputCycles, 1):
                    print(f"    cycle {i}: {' -> '.join(cycle)}")
            self.assertEqual(len(inputCycles) + len(outputCycles), 0, msg='exits cycles detected!')

    def tearDown(self):
        pass
