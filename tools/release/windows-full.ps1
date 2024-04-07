# Licensed under the GNU Lesser General Public License v. 3 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/lgpl-3.0.html
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
# @file        windows-full.ps1
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-01-06     xqyjlj       initial version
#

[CmdletBinding()]
param (
    [string] ${lite_dir} = "litedir", [string] ${full_dir} = "fulldir", [string] ${arch} = "x86"
)

${xmake_version} = "v2.8.6"
${xmake_url} = ""
if (${arch}.Equals("x64")) {
    ${xmake_url} = "https://github.com/xmake-io/xmake/releases/download/" + ${xmake_version} + "/xmake-" + ${xmake_version} + ".win64.zip"
}
else {
    ${xmake_url} = "https://github.com/xmake-io/xmake/releases/download/" + ${xmake_version} + "/xmake-" + ${xmake_version} + ".win32.zip"
}

${git_version} = "2.43.0"
${git_url} = ""
if (${arch}.Equals("x64")) {
    ${git_url} = "https://github.com/git-for-windows/git/releases/download/v" + ${git_version} + ".windows.1/MinGit-" + ${git_version} + "-64-bit.zip"
}
else {
    ${git_url} = "https://github.com/git-for-windows/git/releases/download/v" + ${git_version} + ".windows.1/MinGit-" + ${git_version} + "-32-bit.zip"
}

function Main() {
    copy-Item ${lite_dir} ${full_dir} -Recurse
    Push-Location ${full_dir}

    New-Item -ItemType Directory tools -Force

    Push-Location tools
    # install xmake
    Invoke-WebRequest -Uri ${xmake_url} -OutFile "xmake.zip"
    Expand-Archive -Path "xmake.zip" -DestinationPath "." -Force
    # install git
    Invoke-WebRequest -Uri ${git_url} -OutFile "git.zip"
    Expand-Archive -Path "git.zip" -DestinationPath "git" -Force
    Remove-Item ./*.zip
    Pop-Location

    Pop-Location
}

Main
