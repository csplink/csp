#!/bin/bash

#
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
# Copyright (C) 2023-2024 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        linux-lite.sh
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-01-06     xqyjlj       initial version
#

set -v

dir=${1}
target=${2}
buildir=${3}

mkdir -pv ${dir}
cp -rfv ${buildir}/apps/dev/${target} ${dir}/
pushd ${dir}
deps=$(ldd ${target} | awk '{if (match($3,"/")){ printf("%s "),$3 } }')
mkdir -pv libs
cp -rfv ${deps} libs/
popd

cp -rfv ${buildir}/apps/dev/fonts ${dir}/
cp -rfv ${buildir}/apps/dev/repo ${dir}/
mkdir -pv ${dir}/translations
cp -rfv ${buildir}/apps/dev/translations/*.qm ${dir}/translations
cp -rfv ${buildir}/apps/dev/tools ${dir}/

set +v
