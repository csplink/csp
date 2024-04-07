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
# @file        windows-lite.ps1
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-01-06     xqyjlj       initial version
#

[CmdletBinding()]
param (
    [string] ${dir} = "csp", [string] ${target} = "csp-dev.exe", [string] ${buildir} = "build"
)

function Main() {
    New-Item -ItemType Directory ${dir}
    Copy-Item ${buildir}/apps/dev/${target} ${dir}/

    Push-Location ${dir}
    windeployqt ${target}
    Pop-Location

    Copy-Item ${buildir}/apps/dev/fonts ${dir}/ -Recurse
    Copy-Item ${buildir}/apps/dev/repo ${dir}/ -Recurse
    Copy-Item ${buildir}/apps/dev/translations/*.qm ${dir}/translations -Recurse
}

Main
