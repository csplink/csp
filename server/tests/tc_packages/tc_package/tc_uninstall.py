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
# @file        tc_uninstall.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-12-18     xqyjlj       initial version
#

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from packages.package import Package
from utils.sys import SYS_UTILS

resources_folder = SYS_UTILS.exe_folder() / "tests" / "resources" / "packages"
hal_pack_folder = resources_folder / "hal-pack"
toolchains_pack_folder = resources_folder / "toolchains-pack"


class TestPackageUninstall(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.package = Package()

        # Create mock packages folder structure
        self.packages_dir = self.test_dir / "packages"

        self.patcher_packages_folder = patch(
            "utils.sys.SysUtils.packages_folder",
            return_value=self.packages_dir,
        )

        self.mock_packages_folder = self.patcher_packages_folder.start()

        self.addCleanup(self.patcher_packages_folder.stop)

    def tearDown(self):
        """Clean up after each test method."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_uninstall_hal_package(self):
        """Test uninstalling hal package."""
        # Create packages directory structure
        hal_dir = self.packages_dir / "hal" / "geehy" / "csp_hal_apm32f1" / "latest"

        # Copy package files
        shutil.copytree(hal_pack_folder, hal_dir)

        # Create index file
        self.package.index().origin.setdefault("hal", {}).setdefault(
            "csp_hal_apm32f1", {}
        )["latest"] = hal_dir.absolute().as_posix()
        self.package.save()

        # Verify package exists
        self.assertTrue(hal_dir.exists())

        # Uninstall package
        result = self.package.uninstall("hal", "csp_hal_apm32f1", "latest")

        # Uninstall should succeed
        self.assertTrue(result)

        # Package directory should be removed
        self.assertFalse(hal_dir.exists())

        package_path = self.package.index().path("hal", "csp_hal_apm32f1", "latest")
        self.assertEqual(None, package_path)

    def test_uninstall_toolchains_package(self):
        """Test uninstalling toolchains package."""
        # Create packages directory structure
        toolchains_dir = (
            self.packages_dir / "toolchains" / "arm" / "gcc-arm-none-eabi" / "10.2.1"
        )

        # Copy package files
        shutil.copytree(toolchains_pack_folder, toolchains_dir)

        # Create index entry
        self.package.index().origin.setdefault("toolchains", {}).setdefault(
            "gcc-arm-none-eabi", {}
        )["10.2.1"] = toolchains_dir.absolute().as_posix()
        self.package.save()

        # Verify package exists
        self.assertTrue(toolchains_dir.exists())

        # Uninstall package
        result = self.package.uninstall("toolchains", "gcc-arm-none-eabi", "10.2.1")

        # Uninstall should succeed
        self.assertTrue(result)

        # Package directory should be removed
        self.assertFalse(toolchains_dir.exists())

        package_path = self.package.index().path(
            "toolchains", "gcc-arm-none-eabi", "10.2.1"
        )
        self.assertEqual(None, package_path)

    def test_uninstall_nonexistent_package(self):
        """Test uninstalling a package that doesn't exist."""
        # Mock logger to suppress output
        with patch("loguru.logger.error") as mock_error:
            # Try to uninstall non-existent package
            result = self.package.uninstall("nonexistent", "package", "1.0.0")

            # Uninstall should fail
            self.assertFalse(result)

            # Error should be logged
            mock_error.assert_called()


if __name__ == "__main__":
    unittest.main()
