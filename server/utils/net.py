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
# @file        net.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-07-07     xqyjlj       initial version
#

import socket


class NetUtils:
    @staticmethod
    def check_local_port_used(port):
        """Check if a given port is in use on localhost.

        This function will connect to the given port on localhost and return True
        if the connection is successful, indicating the port is in use.

        Parameters
        ----------
        port : int
            The port to check.

        Returns
        -------
        bool
            True if the port is in use, False otherwise.

        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("localhost", port)) == 0

    @staticmethod
    def find_local_available_port(start_port):
        """Find an available port starting from the given port.

        This function will start at the given port and check if it is available.
        If it is not available, it will increment the port and try again until
        an available port is found.

        Parameters
        ----------
        start_port : int
            The port to start checking from.

        Returns
        -------
        int
            The first available port.

        """
        port = start_port
        while NetUtils.check_local_port_used(port):
            port += 1
        return port
