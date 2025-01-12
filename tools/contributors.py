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
# 2024-08-31     xqyjlj       initial version
#

import os
import shutil

import filetype
import requests
import yaml

__rootDir = os.path.join(os.path.dirname(__file__), "..")
__owner = "csplink"
__repo = "csp"
__token = os.getenv("GITHUB_CSPLINK_DEVELOPER_TOKEN", "None")


class Contributors:

    @staticmethod
    def getUser(name: str):
        url = f"https://api.github.com/users/{name}"
        resp = requests.get(url)
        json = resp.json()
        return json

    @staticmethod
    def getContributors(owner: str, repo: str, token: str):
        url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
        headers = {"Authorization": f"token {token}"}
        resp = requests.get(url, headers=headers)
        json = resp.json()
        names = []
        for info in json:
            names.append(info["login"])
        if 'HalfSweet' not in names:  # for branch stable/cpp-qt
            userInfo = Contributors.getUser('HalfSweet')
            json.append({
                'login': userInfo['login'],
                'avatar_url': userInfo['avatar_url'],
                'html_url': userInfo['html_url'],
                'id': userInfo['id'],
                'contributions': 1
            })

        return sorted(json, key=lambda x: x['contributions'], reverse=True)

    @staticmethod
    def generate(root: str, owner: str, repo: str, token: str):
        contributors = Contributors.getContributors(owner, repo, token)

        avatarFolder = os.path.join(root, "resource", "contributors", "avatar")
        if os.path.isdir(avatarFolder):
            shutil.rmtree(avatarFolder)
        os.makedirs(avatarFolder)

        contributorList = []

        for contributor in contributors:
            response = requests.get(contributor["avatar_url"])
            extension = filetype.guess_extension(response.content)
            extension = f".{extension}" if extension else ""
            file = f"{avatarFolder}/{contributor['id']}{extension}"
            with open(file, 'wb') as fp:
                fp.write(response.content)
            print(f"Author: {contributor['login']}, Contributions: {contributor['contributions']}")
            contributorList.append({
                "name": contributor["login"],
                "avatar": f"avatar/{os.path.basename(file)}",
                "htmlUrl": contributor["html_url"],
                "contributions": contributor["contributions"],
            })

        with open(f"{os.path.join(os.path.dirname(avatarFolder), 'contributors')}", 'w', encoding='utf-8') as f:
            f.write(yaml.dump(contributorList))


if __name__ == "__main__":
    Contributors.generate(__rootDir, __owner, __repo, __token)
