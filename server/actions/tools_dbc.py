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
# @file        tools_dbc.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-03     xqyjlj       initial version
#

import json

import cantools
from cantools.database.can.database import Database
from loguru import logger


def _action_tools_candb_dump(path: str) -> dict:
    result = {}
    try:
        db = cantools.database.load_file(path)
    except Exception as e:
        logger.critical(e)
        return result

    if isinstance(db, Database):
        nodes = {}
        for node in db.nodes:
            nodes[node.name] = {
                "name": node.name,
                "comment": node.comment,
            }

        messages = {}
        for message in db.messages:
            signals = {}
            for sig in message.signals:
                signals[sig.name] = {
                    "name": sig.name,
                    "start": sig.start,
                    "length": sig.length,
                    "byte_order": sig.byte_order,
                    "is_signed": sig.is_signed,
                    "raw_initial": sig.raw_initial,
                    "conversion": {
                        "scale": sig.conversion.scale,
                        "offset": sig.conversion.offset,
                    },
                    "minimum": sig.minimum,
                    "maximum": sig.maximum,
                    "unit": sig.unit,
                    "is_multiplexer": sig.is_multiplexer,
                    "multiplexer_ids": sig.multiplexer_ids,
                    "choices": sig.choices,
                    "spn": sig.spn,
                    "comment": sig.comment,
                    "receivers": sig.receivers,
                }
            messages[message.name] = {
                "name": message.name,
                "id": message.frame_id,
                "idx": f"0x{message.frame_id:x}",
                "is_extended_frame": message.is_extended_frame,
                "length": message.length,
                "comment": message.comment,
                "signals": signals,
            }
        result["nodes"] = nodes
        result["messages"] = messages

    return result


def action_tools_candb_dump(path: str, dump: str) -> dict | None:
    dbc = _action_tools_candb_dump(path)

    if dump == "json":
        print(json.dumps(dbc, indent=2, ensure_ascii=False))
    elif dump == "std":
        for node_name, node in dbc["nodes"].items():
            print(f"node({node_name!r}, {node['comment']!r})")

        print("")

        for message_name, message in dbc["messages"].items():
            print(
                f"message("
                f"{message_name!r}, "
                f"{message['idx']}, "
                f"{message['is_extended_frame']}, "
                f"{message['length']}, "
                f"{message['comment']}"
                ")"
            )
            for signal_name, signal in message["signals"].items():
                print(
                    f"  signal("
                    f"{signal_name!r}, "
                    f"{signal['start']}, "
                    f"{signal['length']}, "
                    f"{signal['byte_order']!r}, "
                    f"{signal['is_signed']}, "
                    f"{signal['raw_initial']}, "
                    f"{signal['conversion']['scale']}, "
                    f"{signal['conversion']['offset']}, "
                    f"{signal['minimum']}, "
                    f"{signal['maximum']}, "
                    f"{signal['unit']!r}, "
                    f"{signal['is_multiplexer']}, "
                    f"{signal['multiplexer_ids']}, "
                    f"{signal['choices']}, "
                    f"{signal['spn']}, "
                    f"{signal['comment']}, "
                    f"{signal['receivers']}"
                    ")"
                )

            print("")
    else:
        return dbc
