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
# @file        coder_generate.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-07-29     xqyjlj       initial version
#

import os

import proto.sio_coder_generate_pb2 as sio_coder_generate_pb2
from coder.coder import Coder
from flask_socketio import SocketIO, emit
from gevent.lock import Semaphore
from public.csp.project import Project
from tqdm import tqdm
from utils.summary import SummaryUtils

__lock = Semaphore()


class __Slot:
    def __init__(self):
        self.__generated_bar = None
        self.sid = ""
        self.socketio: SocketIO | None = None

    def on_generate_progress(self, sender, **kwargs):
        write = kwargs["write"]
        count = kwargs["count"]
        index = kwargs["index"]
        file = kwargs["file"]
        if self.__generated_bar is None:
            self.__generated_bar = tqdm(total=count, desc="generate", unit="file")
        self.__generated_bar.set_description(f"generate {os.path.basename(file)}")
        self.__generated_bar.n = index
        self.__generated_bar.refresh()

        if index == count:
            self.__generated_bar.set_description("generate")
            self.__generated_bar.close()
            self.__generated_bar = None

    def on_sio_generate_progress(self, sender, **kwargs):
        write = kwargs["write"]
        count = kwargs["count"]
        index = kwargs["index"]
        file = kwargs["file"]
        progress = sio_coder_generate_pb2.SioCoderGenerateProgress(
            count=count,
            index=index,
            file=file,
            write=write,
        )
        emit(
            "coder/generate.progress",
            progress.SerializeToString(),
            to=self.sid,
        )
        if self.socketio:
            self.socketio.sleep(0)

    def on_generate(self, sender, **kwargs):
        write = kwargs["write"]
        count = kwargs["count"]
        index = kwargs["index"]
        file = kwargs["file"]

        if write:
            print(
                f"[{index}/{count}] generate {file!r}, because the file or config has been modified."
            )
        else:
            print(
                f"[{index}/{count}] skip {file!r}, because the file or config has not been modified."
            )


def _action_coder_generate(
    project: Project,
    path: str | None,
    progress: bool,
    files: list[str] | None,
    sid: str | None,
    socketio: SocketIO | None = None,
) -> bool:
    summary = SummaryUtils.load_summary(project.vendor, project.targetChip)
    coder = Coder(project, summary)
    slot = __Slot()
    if sid:
        slot.sid = sid
        slot.socketio = socketio
        coder.emitter["generate"].connect(slot.on_sio_generate_progress)
    else:
        if progress:
            coder.emitter["generate"].connect(slot.on_generate_progress)
        else:
            coder.emitter["generate"].connect(slot.on_generate)

    if isinstance(files, list):
        if len(files) == 1 and files[0] == "all":
            files = None
    coder.generate(path, files)

    return True


def action_coder_generate(
    project: Project,
    path: str | None,
    progress: bool,
    files: list[str] | None = None,
    sid: str | None = None,
    socketio: SocketIO | None = None,
) -> bool:
    with __lock:
        return _action_coder_generate(project, path, progress, files, sid, socketio)
