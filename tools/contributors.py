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
# @file        contributors.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-07-28     xqyjlj       initial version
#

import os
import shutil

import requests
from ruamel.yaml import YAML

__root_dir = os.path.join(os.path.dirname(__file__), "..")
__owner = "csplink"
__repo = "csp"
__token = os.getenv("GITHUB_CSPLINK_DEVELOPER_TOKEN", "None")


class Contributors:

    @staticmethod
    def get_user(name: str):
        url = f"https://api.github.com/users/{name}"
        resp = requests.get(url)
        json = resp.json()
        return json

    @staticmethod
    def get_contributors(owner: str, repo: str, token: str):
        url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
        headers = {"Authorization": f"token {token}"}
        resp = requests.get(url, headers=headers)
        assert resp.status_code == 200, "get contributors failed"
        json = resp.json()
        names = []
        for info in json:
            names.append(info["login"])
        if "HalfSweet" not in names:  # for branch stable/cpp-qt
            user_info = Contributors.get_user("HalfSweet")
            json.append(
                {
                    "login": user_info["login"],
                    "avatar_url": user_info["avatar_url"],
                    "html_url": user_info["html_url"],
                    "id": user_info["id"],
                    "contributions": 1,
                }
            )

        return sorted(json, key=lambda x: x["contributions"], reverse=True)

    @staticmethod
    def generate(root: str, owner: str, repo: str, token: str):
        contributors = Contributors.get_contributors(owner, repo, token)

        avatar_folder = os.path.join(root, "resources", "contributors", "avatar")
        if os.path.isdir(avatar_folder):
            shutil.rmtree(avatar_folder)
        os.makedirs(avatar_folder)

        contributor_list = []

        for contributor in contributors:
            response = requests.get(contributor["avatar_url"])
            file = f"{avatar_folder}/{contributor['id']}"
            with open(file, "wb") as fp:
                fp.write(response.content)
            print(
                f"Author: {contributor['login']}, Contributions: {contributor['contributions']}"
            )
            contributor_list.append(
                {
                    "name": contributor["login"],
                    "avatar": f"avatar/{os.path.basename(file)}",
                    "htmlUrl": contributor["html_url"],
                    "contributions": contributor["contributions"],
                }
            )

        with open(
            f"{os.path.join(os.path.dirname(avatar_folder), 'contributors')}",
            "w",
            encoding="utf-8",
        ) as f:
            YAML().dump(contributor_list, f)


if __name__ == "__main__":
    Contributors.generate(__root_dir, __owner, __repo, __token)
