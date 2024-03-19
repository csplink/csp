/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ProjectTable.cpp
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

#include "Configure.h"
#include "ProjectTable.h"
#include "os.h"
#include "qtjson.h"

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ProjectTable::pin_config_t, function, comment, locked, function_property)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ProjectTable::core_t, hal, target, package, company, type, toolchains, modules)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ProjectTable::mdk_arm_t, device, pack, pack_url, cmsis_core)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE_MAYBE_UNUSED(ProjectTable::target_project_t, mdk_arm)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE_MAYBE_UNUSED(ProjectTable::project_t, name, version, target, core, pin_configs,
                                                target_project)
} // namespace nlohmann

#include <QDebug>

QT_DEBUG_ADD_TYPE(ProjectTable::pin_config_t)
QT_DEBUG_ADD_TYPE(ProjectTable::core_t)
QT_DEBUG_ADD_TYPE(ProjectTable::mdk_arm_t)
QT_DEBUG_ADD_TYPE(ProjectTable::target_project_t)
QT_DEBUG_ADD_TYPE(ProjectTable::project_t)

ProjectTable::ProjectTable() = default;

ProjectTable::~ProjectTable() = default;

void ProjectTable::load_project(project_t *proj, const QString &path)
{
    Q_ASSERT(proj != nullptr);
    Q_ASSERT(!path.isEmpty());
    Q_ASSERT(os::isfile(path));

    try
    {
        const std::string buffer = os::readfile(path).toStdString();
        const nlohmann::json json = nlohmann::json::parse(buffer);
        json.get_to(*proj);

        set_value(*proj);
    }
    catch (std::exception &e)
    {
        const QString str = QString("try to parse file \"%1\" failed. \n\nreason: %2").arg(path, e.what());
        qCritical().noquote() << str;
        os::show_error_and_exit(str);
        throw;
    }
}

void ProjectTable::save_project(ProjectTable::project_t &p, const QString &path)
{
    Q_ASSERT(!path.isEmpty());

    const auto json = dump_project(p);
    os::writefile(path, json.toUtf8());
}

QString ProjectTable::dump_project(ProjectTable::project_t &proj)
{
    set_value(proj);
    const nlohmann::json j = proj;
    return QString::fromStdString(j.dump(2));
}

void ProjectTable::set_value(ProjectTable::project_t &proj)
{
    if (proj.target.isEmpty())
    {
        proj.target = "xmake";
    }
    if (proj.core.toolchains.isEmpty())
    {
        proj.core.toolchains = "arm-none-eabi";
    }
    proj.version = QString("v%1").arg(CONFIGURE_PROJECT_VERSION);
    /* 填充 modules */
    {
        proj.core.modules.clear();
        auto pin_configs_i = proj.pin_configs.constBegin();
        while (pin_configs_i != proj.pin_configs.constEnd())
        {
            const pin_config_t &config = pin_configs_i.value();

            if (config.locked)
            {
                const QStringList list = config.function.split("-");
                proj.core.modules << list[0];
            }

            ++pin_configs_i;
        }

        proj.core.modules.removeDuplicates();
    }
}