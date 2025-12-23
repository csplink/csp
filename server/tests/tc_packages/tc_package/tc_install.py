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
# @file        tc_install.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-12-18     xqyjlj       initial version
#

import shutil
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from packages.description import PackageDescription
from packages.package import Package
from utils.io import IO_UTILS
from utils.sys import SYS_UTILS

resources_folder = SYS_UTILS.exe_folder() / "tests" / "resources" / "packages"
hal_pack_folder = resources_folder / "hal-pack"
toolchains_pack_folder = resources_folder / "toolchains-pack"
hal_pack_targz_file = resources_folder / "hal-pack.targz.csppack"
hal_pack_zip_file = resources_folder / "hal-pack.zip.csppack"
toolchains_pack_targz_file = resources_folder / "toolchains-pack.targz.csppack"
toolchains_pack_zip_file = resources_folder / "toolchains-pack.zip.csppack"
invalid_zip_file = resources_folder / "invalid.zip.csppack"
invalid_targz_file = resources_folder / "invalid.targz.csppack"
invalid_pdsc_zip_file = resources_folder / "invalid_pdsc.zip.csppack"
invalid_pdsc_targz_file = resources_folder / "invalid_pdsc.targz.csppack"


class TestPackageInstall(unittest.TestCase):
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

    def test_install_nonexistent_path(self):
        """Test installing from nonexistent path."""

        nonexistent_path = self.test_dir / "nonexistent"

        result = self.package.install(nonexistent_path)
        self.assertIsNone(result)

    def test_install_from_invalid_file(self):
        """Test installing from an invalid text file (not a valid package format)."""

        # Create a simple text file that's not a valid package
        invalid_file = self.test_dir / "invalid.txt"
        # Use current time as random content

        current_time = time.time()
        invalid_file.write_text(f"Invalid file at {current_time}\nNot a package!")

        # Mock logger.error to capture error messages
        with patch("loguru.logger.error") as mock_error:
            result = self.package.install(invalid_file)

            # Installation should fail
            self.assertIsNone(result)

            # Error should be logged
            mock_error.assert_called()

            # Check that error message mentions unsupported file type or invalid format
            error_args = mock_error.call_args[0]
            self.assertTrue(len(error_args) > 0)

    def test_install_from_invalid_csppack_no_description(self):
        """Test installing from csppack file without package description."""
        # Test with both zip and targz formats
        for invalid_file in [invalid_zip_file, invalid_targz_file]:
            with self.subTest(file=invalid_file):
                # Mock logger.error to capture error messages
                with patch("loguru.logger.error") as mock_error:
                    result = self.package.install(invalid_file)

                    # Installation should fail
                    self.assertIsNone(result)

                    # Error should be logged
                    mock_error.assert_called()

                    # Check packages dir content after installation
                    after_content = IO_UTILS.filedirs(self.packages_dir)

                    # Should not have any permanent package installation (only tmp folders allowed)
                    self.assertListEqual(after_content, [self.packages_dir / "tmp"])

    def test_install_from_invalid_csppack_with_invalid_description(self):
        """Test installing from csppack file with invalid package description."""
        # Test with both zip and targz formats
        for invalid_file in [invalid_pdsc_zip_file, invalid_pdsc_targz_file]:
            with self.subTest(file=invalid_file):
                # Mock logger.error to capture error messages
                with patch("loguru.logger.error") as mock_error:
                    result = self.package.install(invalid_file)

                    # Installation should fail
                    self.assertIsNone(result)

                    # Error should be logged
                    mock_error.assert_called()

                    # Check packages dir content after installation
                    after_content = IO_UTILS.filedirs(self.packages_dir)

                    # Should not have any permanent package installation (only tmp folders allowed)
                    self.assertListEqual(after_content, [self.packages_dir / "tmp"])

    def test_install_from_valid_hal_pack(self):
        """Test installing from valid hal pack files (both zip and targz)."""
        # Test with both zip and targz formats
        for pack_file in [hal_pack_zip_file, hal_pack_targz_file]:
            with self.subTest(file=pack_file):
                result = self.package.install(pack_file)

                # Installation should succeed
                self.assertIsNotNone(result)
                self.assertIsInstance(result, PackageDescription)

                package_path = self.package.index().path(
                    "hal", "csp_hal_apm32f1", "latest"
                )

                # Check that package was installed correctly
                expected_path = (
                    self.packages_dir / "hal" / "geehy" / "csp_hal_apm32f1" / "latest"
                )
                self.assertTrue(expected_path.exists())
                self.assertTrue((expected_path / "csp_hal_apm32f1.csppdsc").exists())
                self.assertEqual(package_path, expected_path)

    def test_install_from_valid_toolchains_pack(self):
        """Test installing from valid toolchains pack files (both zip and targz)."""
        # Test with both zip and targz formats
        for pack_file in [toolchains_pack_zip_file, toolchains_pack_targz_file]:
            with self.subTest(file=pack_file):
                result = self.package.install(pack_file)

                # Installation should succeed
                self.assertIsNotNone(result)
                self.assertIsInstance(result, PackageDescription)

                package_path = self.package.index().path(
                    "toolchains", "gcc-arm-none-eabi", "10.2.1"
                )

                # Check that package was installed correctly
                expected_path = (
                    self.packages_dir
                    / "toolchains"
                    / "arm"
                    / "gcc-arm-none-eabi"
                    / "10.2.1"
                )
                self.assertTrue(expected_path.exists())
                self.assertTrue((expected_path / "arm-none-eabi.csppdsc").exists())
                self.assertEqual(package_path, expected_path)

    def test_install_from_hal_pack_directory(self):
        """Test installing from hal pack directory."""
        result = self.package.install(hal_pack_folder)

        # Installation should succeed
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PackageDescription)

        package_path = self.package.index().path("hal", "csp_hal_apm32f1", "latest")

        # Check that package was installed correctly
        expected_path = (
            self.packages_dir / "hal" / "geehy" / "csp_hal_apm32f1" / "latest"
        )
        self.assertTrue(expected_path.exists())
        self.assertTrue((expected_path / "csp_hal_apm32f1.csppdsc").exists())
        self.assertEqual(package_path, expected_path)

    def test_install_from_toolchains_pack_directory(self):
        """Test installing from toolchains pack directory."""
        result = self.package.install(toolchains_pack_folder)

        # Installation should succeed
        self.assertIsNotNone(result)
        self.assertIsInstance(result, PackageDescription)

        package_path = self.package.index().path(
            "toolchains", "gcc-arm-none-eabi", "10.2.1"
        )

        # Check that package was installed correctly
        expected_path = (
            self.packages_dir / "toolchains" / "arm" / "gcc-arm-none-eabi" / "10.2.1"
        )
        self.assertTrue(expected_path.exists())
        self.assertTrue((expected_path / "arm-none-eabi.csppdsc").exists())
        self.assertEqual(package_path, expected_path)


if __name__ == "__main__":
    unittest.main()
