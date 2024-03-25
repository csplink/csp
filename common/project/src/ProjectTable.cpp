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
#include "QtJson.h"

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ProjectTable::PinConfigType, Function, Comment, Locked, FunctionProperty)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ProjectTable::MdkArmType, Device, Pack, PackUrl, CmsisCore)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE_MAYBE_UNUSED(ProjectTable::TargetProjectType, MdkArm)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE_MAYBE_UNUSED(ProjectTable::ProjectType, Company, Hal, HalVersion, Modules, Package,
                                                TargetChip, Toolchains, ToolchainsVersion, Type, Name, PinConfigs, TargetProject,
                                                TargetProjectConfig, Version)
} // namespace nlohmann

#include <QDebug>

QT_DEBUG_ADD_TYPE(ProjectTable::PinConfigType)
QT_DEBUG_ADD_TYPE(ProjectTable::MdkArmType)
QT_DEBUG_ADD_TYPE(ProjectTable::TargetProjectType)
QT_DEBUG_ADD_TYPE(ProjectTable::ProjectType)

ProjectTable::ProjectTable() = default;

ProjectTable::~ProjectTable() = default;

void ProjectTable::loadProject(ProjectType *project, const QString &path)
{
    if (project != nullptr)
    {
        QFile file(path);
        if (file.open(QIODevice::ReadOnly))
        {
            try
            {
                const std::string buffer = file.readAll().toStdString();
                const nlohmann::json json = nlohmann::json::parse(buffer);
                json.get_to(*project);
            }
            catch (std::exception &e)
            {
                const QString str = QString("try to parse file \"%1\" failed. \n\nreason: %2").arg(path, e.what());
                qCritical().noquote() << str;
                throw;
            }

            file.close();

            setValue(*project);
        }
        else
        {
            /** TODO: failed */
        }
    }
    else
    {
        /** TODO: failed */
    }
}

void ProjectTable::saveProject(ProjectType &project, const QString &path)
{
    const auto json = dumpProject(project);

    QFile file(path);
    if (file.open(QIODevice::WriteOnly))
    {
        file.write(json.toUtf8());
        file.close();
    }
}

QString ProjectTable::dumpProject(ProjectType &project)
{
    setValue(project);
    const nlohmann::json j = project;
    return QString::fromStdString(j.dump(2));
}

void ProjectTable::setValue(ProjectType &project)
{
    if (project.TargetProject.isEmpty())
    {
        project.TargetProject = "XMake";
    }
    if (project.Toolchains.isEmpty())
    {
        project.Toolchains = "arm-none-eabi";
    }
    project.Version = QString("v%1").arg(CONFIGURE_PROJECT_VERSION);
    /* 填充 modules */
    {
        project.Modules.clear();
        auto pin_configs_i = project.PinConfigs.constBegin();
        while (pin_configs_i != project.PinConfigs.constEnd())
        {
            const PinConfigType &config = pin_configs_i.value();

            if (config.Locked)
            {
                const QStringList list = config.Function.split("-");
                project.Modules << list[0];
            }

            ++pin_configs_i;
        }

        project.Modules.removeDuplicates();
    }
}
