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

${python_version} = "3.10.11"
${python_url} = ""
if (${arch}.Equals("x64")) {
    ${python_url} = "https://www.python.org/ftp/python/" + ${python_version} + "/python-" + ${python_version} + "-embed-amd64.zip"
}
else {
    ${python_url} = "https://www.python.org/ftp/python/" + ${python_version} + "/python-" + ${python_version} + "-embed-win32.zip"
}

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
    # install python
    Invoke-WebRequest -Uri ${python_url} -OutFile "python.zip"
    Expand-Archive -Path "python.zip" -DestinationPath "python" -Force
    Push-Location python
    ${content} = Get-Content python310._pth
    ${new_content} = ${content} -replace '#import site', 'import site'
    Set-Content python310._pth -Value ${new_content}
    Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile "get-pip.py"
    $Env:PATH = $PWD.Path + "/Scripts;$Env:PATH"
    ./python --version
    ./python ./get-pip.py
    Remove-Item ./get-pip.py
    ./Scripts/pip3 -r ${CI_PROJECT_DIR}/tools/release/requirements.txt
    Pop-Location

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
