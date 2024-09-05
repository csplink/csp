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
import requests, os, filetype, shutil, yaml

rootDir = os.path.join(os.path.dirname(__file__), "..")


def getContributors(owner, repo, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    contributors = response.json()
    return sorted(contributors, key=lambda x: x['contributions'], reverse=True)


owner = "csplink"
repo = "csp"
token = os.getenv("GITHUB_CSPLINK_DEVELOPER_TOKEN", "None")
contributors = getContributors(owner, repo, token)

avatarFolder = os.path.join(rootDir, "resource", "contributors", "avatar")
if os.path.isdir(avatarFolder):
    shutil.rmtree(avatarFolder)
os.makedirs(avatarFolder)

contributorList = []

for contributor in contributors:
    response = requests.get(contributor["avatar_url"])
    path = os.path.join(avatarFolder, f"resource", "contributors", "avatar")
    extension = filetype.guess_extension(response.content)
    extension = f".{extension}" if extension else ""
    file = f"{avatarFolder}/{contributor['id']}{extension}"
    with open(file, 'wb') as fp:
        fp.write(response.content)
    contributorList.append({
        "name": contributor["login"],
        "avatar": f"avatar/{os.path.basename(file)}",
        "html_url": contributor["html_url"],
        "contributions": contributor["contributions"],
    })

with open(f"{os.path.join(os.path.dirname(avatarFolder), 'contributors')}", 'w', encoding='utf-8') as f:
    f.write(yaml.dump(contributorList))
