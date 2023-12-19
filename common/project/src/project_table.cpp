/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        project_table.cpp
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
 *  2023-05-27     xqyjlj       initial version
 */

#include <QDebug>
#include <QFile>

#include "os.h"
#include "project_table.h"
#include "qtjson.h"

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(project_table::pin_config_t, function, comment, locked, function_property)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(project_table::core_t, name, hal, target, package, company, type, toolchains,
                                   modules)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(project_table::project_t, core, pin_configs)
} // namespace nlohmann

#include <QDebug>

QT_DEBUG_ADD_TYPE(project_table::pin_config_t)

project_table::project_table() = default;

project_table::~project_table() = default;

void project_table::load_project(project_t *project, const QString &path)
{
    Q_ASSERT(project != nullptr);
    Q_ASSERT(!path.isEmpty());
    Q_ASSERT(os::isfile(path));

    try
    {
        const std::string buffer = os::readfile(path).toStdString();
        const nlohmann::json json = nlohmann::json::parse(buffer);
        json.get_to(*project);
    }
    catch (std::exception &e)
    {
        const QString str = QString("try to parse file \"%1\" failed. \n\nreason: %2").arg(path, e.what());
        qCritical() << str;
        os::show_error_and_exit(str);
        throw;
    }
}

void project_table::save_project(const project_table::project_t &p, const QString &path)
{
    Q_ASSERT(!path.isEmpty());

    const auto json = dump_project(p);
    QFile file(path);
    file.open(QFileDevice::WriteOnly | QIODevice::Text);
    file.write(json.toUtf8());
    file.close();
}

QString project_table::dump_project(const project_table::project_t &p)
{
    const nlohmann::json j = p;
    return QString::fromStdString(j.dump(2));
}
