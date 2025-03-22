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
# @file        coder.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-11     xqyjlj       initial version
#

import copy
import glob
import hashlib
import importlib.util
import os
import re
import sys
import time
import xml.etree.ElementTree as etree
from pathlib import Path
from types import ModuleType

import jinja2
from PySide6.QtCore import QObject, Signal
from loguru import logger
from tqdm import tqdm

from .project import PROJECT
from .settings import SETTINGS


def _do_hex(value: int, length: int = 8) -> str:
    return f"0x{value:0{length}X}"


_filters = {
    "hex": _do_hex,
}


class Coder(QObject):
    dump_progress_updated = Signal(str, int, int)
    generate_progress_updated = Signal(str, int, int, bool)
    copy_library_progress_updated = Signal(str, int, int, bool, str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.__context_table = {}
        self.__files = {}
        self.__generator = None

        self.__generator = self.__load_generator()
        self.__files = self.__get_files_table()

    def generate(self, output: str = ""):
        if not self.__check_hal_folder():
            return

        if output is None or not os.path.isdir(output):
            output = os.path.dirname(PROJECT.path())

        files = self.dump()
        count = len(files)
        for index, (path, context) in enumerate(files.items(), start=1):
            gen_md5 = hashlib.md5(context.encode("utf-8")).hexdigest()
            path = f"{output}/{path}".replace("\\", "/")
            if os.path.isfile(path):
                with open(path, "r", encoding="utf-8") as file:
                    file_context = file.read()
                    file_md5 = hashlib.md5(file_context.encode("utf-8")).hexdigest()
            else:
                Path(path).parent.mkdir(parents=True, exist_ok=True)
                file_md5 = ""
            if gen_md5 != file_md5:
                self.generate_progress_updated.emit(path, index, count, True)
                with open(path, "w", encoding="utf-8") as file:
                    file.write(context)
            else:
                self.generate_progress_updated.emit(path, index, count, False)

        for file, info in self.__files.items():
            if not info.get("gen", True):
                path = f"{output}/{file}".replace("\\", "/")
                if os.path.isfile(path):
                    os.remove(path)

        self.__copy_library()

    def dump(self) -> dict:
        package_folder = PROJECT.hal_folder()

        if len(self.__files) == 0:
            return {}

        data = {
            "author": "csplink coder",
            "version": SETTINGS.VERSION,
            "project": PROJECT.project().origin,
            "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "year": time.strftime("%Y", time.localtime()),
            "platform": sys.platform,
        }

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                [
                    f"{SETTINGS.EXE_FOLDER}/resource/templates",
                    f"{package_folder}/tools/generator/templates",
                ]
            ),
            line_comment_prefix="//",
        )

        # env.add_extension("jinja2.ext.i18n")
        env.add_extension("jinja2.ext.debug")
        env.add_extension("jinja2.ext.do")
        env.add_extension("jinja2.ext.loopcontrols")

        if PROJECT.project().gen.use_toolchains_package:
            data["toolchainsPath"] = PROJECT.toolchains_folder()

        files = glob.glob(f"{package_folder}/tools/generator/filters/*.py")
        sys.path = SETTINGS.SYS_PATH + [f"{package_folder}/tools/generator/filters"]
        for file in files:
            spec = importlib.util.spec_from_file_location(Path(file).stem, file)
            if spec is None or spec.loader is None:
                break
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            functions = [
                name for name in dir(module) if callable(getattr(module, name))
            ]
            for fun in functions:
                if not fun.startswith("_"):
                    function = getattr(module, fun)
                    env.filters[fun] = function
        env.filters.update(_filters)

        self.__context_table.clear()
        count = 0
        for file, info in self.__files.items():
            if info.get("gen", True):
                count += 1
        index = 0
        for file, info in self.__files.items():
            if info.get("gen", True):
                index += 1
                self.dump_progress_updated.emit(file, index, count)
                suffix = Path(file).suffix
                context = self.__render(file, info, env, data)
                if context is not None:
                    self.__context_table[file] = context
                elif suffix == ".uvprojx" or suffix == ".uvproj":
                    pass

            # self.dumped.emit(file)

        return self.__context_table

    def deploy(self):
        if self.__generator is None:
            return

        data = self.__generator.deploy(
            copy.deepcopy(PROJECT.project().origin), os.path.dirname(PROJECT.path())
        )
        return data

    def files_list(self) -> list[str]:
        return list(self.__files.keys())

    def __load_generator(self) -> ModuleType | None:
        if self.__check_hal_folder():
            spec = importlib.util.spec_from_file_location(
                "coder", f"{PROJECT.hal_folder()}/tools/generator/generator.py"
            )
            if spec is None or spec.loader is None:
                return None
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        return None

    def __get_files_table(self) -> dict[str, dict[str, str]]:
        if self.__generator is None:
            return {}
        files = self.__generator.files_table(copy.deepcopy(PROJECT.project().origin))
        return files

    def __copy_library(self):
        if self.__generator is None:
            return
        output_dir = os.path.dirname(PROJECT.path())
        self.__generator.copy_library(
            copy.deepcopy(PROJECT.project().origin),
            output_dir,
            self.__emit_copy_library_signal,
        )

    def __emit_copy_library_signal(
        self, path: str, index: int, count: int, success: bool, reason: str
    ):
        self.copy_library_progress_updated.emit(path, index, count, success, reason)

    def __check_hal_folder(self) -> bool:
        if not os.path.isfile(f"{PROJECT.hal_folder()}/tools/generator/generator.py"):
            logger.error(
                f"{PROJECT.hal_folder()} is not directory! maybe package({PROJECT.project().gen.hal}) not yet installed."
            )
            return False
        return True

    def __match_user(
        self, path: str, prefix1: str, suffix1: str, prefix2: str, suffix2: str
    ) -> dict:
        code = {}
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                data = f.read()
                for s in re.findall(
                    f"{prefix1} user code begin (.*), do not change this comment!{suffix1}",
                    data,
                ):
                    matcher = f"{prefix1} user code begin {s}, do not change this comment!{suffix1}\n(.*){prefix2} user code end {s}, do not change this comment!{suffix2}"
                    result = str.rstrip(re.findall(matcher, data, re.S)[0])
                    if result:
                        code[s] = result
                        # code[s] = str.rstrip(result)
                        # # noinspection PyUnresolvedReferences
                        # if code[s] != '':
                        #     code[s] = code[s] + '\n'
                    else:
                        code[s] = ""
        return code

    def __render(
        self, path: str, info: dict, env: jinja2.Environment, args: dict
    ) -> str | None:
        abs_path = f"{PROJECT.folder()}/{path}"
        template_name = info.get("template")
        if template_name is None:
            template_name = f"{os.path.basename(path)}.j2"
        template = env.get_template(template_name)
        suffix = Path(abs_path).suffix
        if suffix == ".h" or suffix == ".c":
            args["userCode"] = self.__match_user(
                abs_path, r"/\*\*<", r" \*/", r"/\*\*>", r" \*/"
            )
        elif Path(abs_path).name == "xmake.lua":
            args["userCode"] = self.__match_user(abs_path, "----<", "", "---->", "")
        elif Path(abs_path).name == "CMakeLists.txt":
            args["userCode"] = self.__match_user(abs_path, "##==<", "", "##==>", "")

        args["file"] = os.path.basename(path)
        args["brief"] = info.get("brief", "file automatically-generated by tool: [csp]")
        context = template.render({"CSP": args})
        context = context.strip() + "\n"

        time_pattern = r"\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\b"  # YYYY-MM-DD HH:MM:SS
        gen_md5 = hashlib.md5(
            re.sub(time_pattern, "", context).encode("utf-8")
        ).hexdigest()
        file_context = ""
        if os.path.isfile(abs_path):
            with open(abs_path, "r", encoding="utf-8") as file:
                file_context = file.read()
                file_md5 = hashlib.md5(
                    re.sub(time_pattern, "", file_context).encode("utf-8")
                ).hexdigest()
        else:
            file_md5 = ""

        if gen_md5 == file_md5:
            context = file_context

        return context

    # def __generateMdkArmProject(self, project: dict, path: str, minVersion: str) -> str:
    #     spec = importlib.util.spec_from_file_location(
    #         "coder", f"{package_dir}/tools/coder/gen_mdk_arm.py"
    #     )
    #     module = importlib.util.module_from_spec(spec)
    #     spec.loader.exec_module(module)

    #     if os.path.isfile(path):
    #         tree = etree.parse(path)
    #     else:
    #         tree = None

    #     return module.main(
    #         copy.deepcopy(project), copy.deepcopy(minVersion), copy.deepcopy(tree)
    #     )


class CoderCmd(QObject):

    def __init__(self, output: str, progress: bool, parent=None):
        super().__init__(parent=parent)

        self.output = output
        self.progress = progress
        self.dumped_bar = None
        self.generated_bar = None
        self.library_copied_bar = None

        self.coder = Coder()
        self.coder.dump_progress_updated.connect(self.__on_coder_dumpProgressUpdated)
        self.coder.generate_progress_updated.connect(
            self.__on_coder_generateProgressUpdated
        )
        self.coder.copy_library_progress_updated.connect(
            self.__on_coder_copyLibraryProgressUpdated
        )

    def __on_coder_dumpProgressUpdated(self, path: str, index: int, count: int):
        if self.progress:
            if self.dumped_bar is None:
                self.dumped_bar = tqdm(total=count, desc="dump", unit="file")
            self.dumped_bar.set_description(f"dump {path}")
            self.dumped_bar.n = index
            self.dumped_bar.refresh()
            if index == count:
                self.dumped_bar.set_description("dump")
                self.dumped_bar.close()

    def __on_coder_generateProgressUpdated(
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
                # print(f'skip {path!r}, because the file or config has not been modified.')
                pass

    def __on_coder_copyLibraryProgressUpdated(
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
