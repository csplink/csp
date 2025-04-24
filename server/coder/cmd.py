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
# @file        cmd.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-07-07     xqyjlj       initial version
#


class CoderCmd(QObject):

    def __init__(self, output: str, progress: bool, parent=None):
        super().__init__(parent=parent)

        self.output = output
        self.progress = progress
        self.dumped_bar = None
        self.generated_bar = None
        self.library_copied_bar = None

        self.coder = Coder()
        self.coder.dump_progress_updated.connect(self.__on_coder_dump_progress_updated)
        self.coder.generate_progress_updated.connect(
            self.__on_coder_generate_progress_updated
        )
        self.coder.copy_library_progress_updated.connect(
            self.__on_coder_copy_library_progress_updated
        )

    def __on_coder_dump_progress_updated(self, path: str, index: int, count: int):
        if self.progress:
            if self.dumped_bar is None:
                self.dumped_bar = tqdm(total=count, desc="dump", unit="file")
            self.dumped_bar.set_description(f"dump {path}")
            self.dumped_bar.n = index
            self.dumped_bar.refresh()
            if index == count:
                self.dumped_bar.set_description("dump")
                self.dumped_bar.close()

    def __on_coder_generate_progress_updated(
        self, path: str, index: int, count: int, success: bool
    ):
        if self.progress:
            if self.generated_bar is None:
                self.generated_bar = tqdm(total=count, desc="generate", unit="file")
            self.generated_bar.set_description(f"generate {os.path.basename(path)}")
            self.generated_bar.n = index
            self.generated_bar.refresh()
            if index == count:
                self.generated_bar.set_description("generate")
                self.generated_bar.close()
        else:
            if success:
                print(
                    f"generate {path!r}, because the file or config has been modified."
                )
            else:
                print(
                    f"skip {path!r}, because the file or config has not been modified."
                )
                pass

    def __on_coder_copy_library_progress_updated(
        self, path: str, index: int, count: int, success: bool, reason: str
    ):
        if self.progress:
            if self.library_copied_bar is None:
                self.library_copied_bar = tqdm(total=count, desc="copy", unit="file")
            self.library_copied_bar.set_description(f"copy {os.path.basename(path)}")
            self.library_copied_bar.n = index
            self.library_copied_bar.refresh()
            if index == count:
                self.library_copied_bar.set_description("copy")
                self.library_copied_bar.close()
        else:
            if success:
                print(f"copy {path!r}, {reason}.")
            else:
                # print(f'skip {path!r}, {reason}.')
                pass

    def gen(self):
        self.coder.generate(self.output)
