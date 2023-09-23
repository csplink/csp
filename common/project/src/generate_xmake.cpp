/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        generate_xmake.cpp
 *  @brief
 *
 * ****************************************************************************
 *  @attention
 *  Licensed under the GNU General Public License v. 3 (the "License");
 *  You may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      https://www.gnu.org/licenses/gpl-3.0.html
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 *  Copyright (C) 2023-2023 xqyjlj<xqyjlj@126.com>
 *
 * ****************************************************************************
 *  Change Logs:
 *  Date           Author       Notes
 *  ------------   ----------   -----------------------------------------------
 *  2023-07-04     xqyjlj       initial version
 */

#include <QDateTime>
#include <QFile>

#include "configure.h"
#include "generate_xmake.h"

generate_xmake::generate_xmake() = default;

generate_xmake::~generate_xmake() = default;

QString generate_xmake::generate(const project_table::project_t &project_table)
{
    QFile      file(":/lib/project/template/xmake.lua");
    const auto date_time    = QDateTime::currentDateTime();
    const auto date         = date_time.toString("yyyy-MM-dd hh:mm:ss");
    const auto version      = CONFIGURE_PROJECT_VERSION;
    const auto project_name = project_table.core[CSP_PROJECT_CORE_NAME];
    const auto hal          = project_table.core[CSP_PROJECT_CORE_HAL];

    file.open(QFileDevice::ReadOnly | QIODevice::Text);
    QString buffer = file.readAll();
    file.close();

    buffer.replace("{{version}}", version);
    buffer.replace("{{date}}", date);
    buffer.replace("{{project}}", project_name);
    buffer.replace("{{hal}}", hal);

    return buffer;
}
