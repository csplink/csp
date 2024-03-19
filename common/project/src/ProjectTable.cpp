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
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ProjectTable::PinConfigType, function, comment, locked, function_property)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ProjectTable::CoreType, hal, target, package, company, type, toolchains, modules)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ProjectTable::MdkArmType, device, pack, pack_url, cmsis_core)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE_MAYBE_UNUSED(ProjectTable::TargetProjectType, mdk_arm)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE_MAYBE_UNUSED(ProjectTable::ProjectType, name, version, target, core, pin_configs,
                                                target_project)
} // namespace nlohmann

#include <QDebug>

QT_DEBUG_ADD_TYPE(ProjectTable::PinConfigType)
QT_DEBUG_ADD_TYPE(ProjectTable::CoreType)
QT_DEBUG_ADD_TYPE(ProjectTable::MdkArmType)
QT_DEBUG_ADD_TYPE(ProjectTable::TargetProjectType)
QT_DEBUG_ADD_TYPE(ProjectTable::ProjectType)

ProjectTable::ProjectTable() = default;

ProjectTable::~ProjectTable() = default;

void ProjectTable::loadProject(ProjectType *project, const QString &path)
{
    Q_ASSERT(project != nullptr);
    Q_ASSERT(!path.isEmpty());
    Q_ASSERT(os::isfile(path));

    try
    {
        const std::string buffer = os::readfile(path).toStdString();
        const nlohmann::json json = nlohmann::json::parse(buffer);
        json.get_to(*project);

        setValue(*project);
    }
    catch (std::exception &e)
    {
        const QString str = QString("try to parse file \"%1\" failed. \n\nreason: %2").arg(path, e.what());
        qCritical().noquote() << str;
        os::show_error_and_exit(str);
        throw;
    }
}

void ProjectTable::saveProject(ProjectType &project, const QString &path)
{
    Q_ASSERT(!path.isEmpty());

    const auto json = dumpProject(project);
    os::writefile(path, json.toUtf8());
}

QString ProjectTable::dumpProject(ProjectType &project)
{
    setValue(project);
    const nlohmann::json j = project;
    return QString::fromStdString(j.dump(2));
}

void ProjectTable::setValue(ProjectType &project)
{
    if (project.target.isEmpty())
    {
        project.target = "xmake";
    }
    if (project.core.toolchains.isEmpty())
    {
        project.core.toolchains = "arm-none-eabi";
    }
    project.version = QString("v%1").arg(CONFIGURE_PROJECT_VERSION);
    /* 填充 modules */
    {
        project.core.modules.clear();
        auto pin_configs_i = project.pin_configs.constBegin();
        while (pin_configs_i != project.pin_configs.constEnd())
        {
            const PinConfigType &config = pin_configs_i.value();

            if (config.locked)
            {
                const QStringList list = config.function.split("-");
                project.core.modules << list[0];
            }

            ++pin_configs_i;
        }

        project.core.modules.removeDuplicates();
    }
}
