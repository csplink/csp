#!/bin/bash

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
# Copyright (C) 2025-2025 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        deploy.sh
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-01-10     xqyjlj       initial version
#

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

function deploy {
    path=${1}

    pushd "${script_dir}"/..

    python tools/lrelease.py
    python tools/contributors.py
    python -m nuitka --standalone --disable-console --windows-icon-from-ico=resource/images/logo.ico --show-memory --show-progress --assume-yes-for-downloads --output-dir=build --onefile --plugin-enable=pyside6 ./csp.py

    mkdir -pv "${path}"
    cp -rfv resource "${path}/"
    rm -rfv "${path}/resource/i18n/csplink.*.ts"
    cp -fv build/csp.exe "${path}/"

    "${path}/csp.exe" --version

    popd
}

