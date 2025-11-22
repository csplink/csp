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
# @file        coder_dump.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-07-29     xqyjlj       initial version
#

import difflib
from pathlib import Path

import proto.sio_coder_dump_pb2 as sio_coder_dump_pb2
from coder.coder import Coder
from flask_socketio import SocketIO, emit
from public.csp.project import Project
from utils.io import IoUtils
from utils.summary import SummaryUtils


class __Slot:

    def __init__(self):
        self.sid = ""
        self.socketio: SocketIO | None = None

    def on_sio_dump_progress(self, sender, **kwargs):
        count = kwargs["count"]
        index = kwargs["index"]
        file = kwargs["file"]

        progress = sio_coder_dump_pb2.SioCoderDumpProgress(
            count=count,
            index=index,
            file=file,
        )
        emit(
            "coder/dump.progress",
            progress.SerializeToString(),
            to=self.sid,
        )
        if self.socketio:
            self.socketio.sleep(0)


def action_coder_dump(
    project: Project,
    diff: bool,
    path: str | None,
    content: dict | None,
    sid: str | None = None,
    socketio: SocketIO | None = None,
) -> dict:
    summary = SummaryUtils.load_summary(project.vendor, project.targetChip)
    coder = Coder(project, summary)

    files = {}

    if sid:
        slot = __Slot()
        slot.sid = sid
        slot.socketio = socketio
        coder.emitter["dump"].connect(slot.on_sio_dump_progress)

    for file, data in coder.dump().items():
        files[file] = {"content": data}

    if diff and path is not None and content is not None:
        for file, data in files.items():
            lines = IoUtils.readlines(str(Path(project.folder()) / file))
            text: str = data["content"]
            dif = difflib.unified_diff(
                lines,
                text.splitlines(keepends=True),
                fromfile=file,
                tofile=file,
                lineterm="",
            )
            files[file]["diff"] = "".join(dif)

    return files
