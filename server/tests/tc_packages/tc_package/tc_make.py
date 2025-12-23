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
# @file        tc_make.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-12-18     xqyjlj       initial version


import shutil
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from packages.description import PackageDescription
from packages.package import Package
from utils.io import IO_UTILS
from utils.sys import SysUtils

hal_pack_folder = (
    SysUtils.exe_folder() / "tests" / "resources" / "packages" / "hal-pack"
)
toolchains_pack_folder = (
    SysUtils.exe_folder() / "tests" / "resources" / "packages" / "toolchains-pack"
)


class TestPackageMake(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.source_dir = self.test_dir / "source"
        self.package = Package()

    def tearDown(self):
        """Clean up after each test method."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_make_hal_package(self):
        """Test making a hal package."""
        self._test_make_package(
            source_folder=hal_pack_folder,
            config_file="csp_hal_apm32f1.csppdsc",
            expected_package_name="csp_hal_apm32f1-latest.csppack",
        )

    @patch("platform.system", return_value="Windows")
    def test_make_toolchains_package_windows(self, _mock_system: MagicMock):
        """Test making a toolchains package on Windows."""
        self._test_make_package(
            source_folder=toolchains_pack_folder,
            config_file="arm-none-eabi.csppdsc",
            expected_package_name="gcc-arm-none-eabi-10.2.1.windows.csppack",
        )

    @patch("platform.system", return_value="Linux")
    def test_make_toolchains_package_linux(self, _mock_system: MagicMock):
        """Test making a toolchains package on Linux."""
        self._test_make_package(
            source_folder=toolchains_pack_folder,
            config_file="arm-none-eabi.csppdsc",
            expected_package_name="gcc-arm-none-eabi-10.2.1.linux.csppack",
        )

    def _test_make_package(
        self, source_folder: Path, config_file: str, expected_package_name: str
    ):
        """Helper method to test package making."""
        # Copy source_folder to source_dir
        if source_folder.exists():
            shutil.copytree(source_folder, self.source_dir, dirs_exist_ok=True)

        result = self.package.make(self.source_dir)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, PackageDescription)

        configs = IO_UTILS.readyaml(self.source_dir / config_file)

        assert result is not None
        self.assertDictEqual(result.origin, configs)

        # Check for generated package file in parent directory
        files = IO_UTILS.files(self.test_dir)
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].name, expected_package_name)

    def test_make_with_invalid_package_description(self):
        """Test making a package with invalid description."""
        # Use empty source directory (no package description)
        result = self.package.make(self.source_dir)
        self.assertIsNone(result)

    @patch("platform.system", return_value="Windows")
    def test_compression_format_windows(self, _mock_system: MagicMock):
        """Test that Windows package is compressed as ZIP format."""
        # Copy hal_pack_folder to source_dir
        if hal_pack_folder.exists():
            shutil.copytree(hal_pack_folder, self.source_dir, dirs_exist_ok=True)

        result = self.package.make(self.source_dir)

        self.assertIsNotNone(result)

        # Find the generated package file
        files = IO_UTILS.files(self.test_dir)
        self.assertEqual(len(files), 1)
        package_file = files[0]

        # Verify it's a ZIP file
        self.assertTrue(package_file.suffix == ".csppack")

        # Try to open it as ZIP
        try:
            with zipfile.ZipFile(package_file, "r") as zf:
                # Check that it contains expected files
                file_list = zf.namelist()
                self.assertIn("csp_hal_apm32f1.csppdsc", file_list)
        except zipfile.BadZipFile:
            self.fail("Package file is not a valid ZIP file")

    @patch("platform.system", return_value="Linux")
    def test_compression_format_linux(self, _mock_system: MagicMock):
        """Test that Linux package is compressed as TAR.GZ format."""
        # Copy hal_pack_folder to source_dir
        if hal_pack_folder.exists():
            shutil.copytree(hal_pack_folder, self.source_dir, dirs_exist_ok=True)

        result = self.package.make(self.source_dir)

        self.assertIsNotNone(result)

        # Find the generated package file
        files = IO_UTILS.files(self.test_dir)
        self.assertEqual(len(files), 1)
        package_file = files[0]

        # Verify it's a TAR.GZ file
        self.assertTrue(package_file.suffix == ".csppack")

        # Try to open it as TAR.GZ
        try:
            with tarfile.open(package_file, "r:gz") as tf:
                # Check that it contains expected files
                file_list = tf.getnames()
                # Look for the .csppdsc file in the list
                found_config = any(
                    "csp_hal_apm32f1.csppdsc" in name for name in file_list
                )
                self.assertTrue(
                    found_config, "Package does not contain expected config file"
                )
        except (tarfile.ReadError, tarfile.CompressionError):
            self.fail("Package file is not a valid TAR.GZ file")

    def _setup_gitignore_test_files(self):
        """Set up test files for gitignore filtering tests."""
        # Copy hal_pack_folder to source_dir
        if hal_pack_folder.exists():
            shutil.copytree(hal_pack_folder, self.source_dir, dirs_exist_ok=True)

        # Create test files that should be ignored
        # File matching *.txt pattern (should be ignored)
        (self.source_dir / "test.txt").write_text(
            "This should be ignored", encoding="utf-8"
        )
        (self.source_dir / "readme.txt").write_text(
            "Another ignored file", encoding="utf-8"
        )

        # File in subfolder matching *.o pattern (should be ignored)
        (self.source_dir / "folder" / "main.o").write_bytes(b"object file")
        (self.source_dir / "folder" / "test.o").write_bytes(b"another object")

        # Create files that should be included
        (self.source_dir / "test.md").write_text(
            "This should be included", encoding="utf-8"
        )
        (self.source_dir / "folder" / "test.c").write_text(
            "// C source file", encoding="utf-8"
        )

    def _check_gitignore_test_files(self, file_list: list[str]):
        # Files that should be included
        self.assertIn("csp_hal_apm32f1.csppdsc", file_list)
        self.assertIn("test.md", file_list)
        self.assertIn("folder/test.c", file_list)

        # Files that should be ignored (by .gitignore)
        self.assertNotIn("test.txt", file_list)
        self.assertNotIn("readme.txt", file_list)
        self.assertNotIn("folder/main.o", file_list)
        self.assertNotIn("folder/test.o", file_list)

    @patch("platform.system", return_value="Windows")
    def test_gitignore_filtering_windows(self, _mock_system: MagicMock):
        """Test that .gitignore files properly filter files during packaging on Windows."""
        # Set up test files
        self._setup_gitignore_test_files()

        result = self.package.make(self.source_dir)

        self.assertIsNotNone(result)

        # Find the generated package file
        files = IO_UTILS.files(self.test_dir)
        self.assertEqual(len(files), 1)
        package_file = files[0]

        # Windows uses ZIP
        try:
            with zipfile.ZipFile(package_file, "r") as zf:
                file_list = zf.namelist()
                self._check_gitignore_test_files(file_list)

        except zipfile.BadZipFile:
            self.fail("Package file is not a valid ZIP file")

    @patch("platform.system", return_value="Linux")
    def test_gitignore_filtering_linux(self, _mock_system: MagicMock):
        """Test that .gitignore files properly filter files during packaging on Linux."""
        # Set up test files
        self._setup_gitignore_test_files()

        result = self.package.make(self.source_dir)

        self.assertIsNotNone(result)

        # Find the generated package file
        files = IO_UTILS.files(self.test_dir)
        self.assertEqual(len(files), 1)
        package_file = files[0]

        # Linux/Mac uses TAR.GZ
        try:
            with tarfile.open(package_file, "r:gz") as tf:
                file_list = tf.getnames()
                self._check_gitignore_test_files(file_list)

        except (tarfile.ReadError, tarfile.CompressionError):
            self.fail("Package file is not a valid TAR.GZ file")


if __name__ == "__main__":
    unittest.main()
