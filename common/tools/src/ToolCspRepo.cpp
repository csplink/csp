/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        ToolCspRepo.cpp
 * @brief
 *
 *****************************************************************************
 * @attention
 * Licensed under the GNU General Public License v. 3 (the "License");
 * You may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.gnu.org/licenses/gpl-3.0.html
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Copyright (C) 2024-2024 xqyjlj<xqyjlj@126.com>
 *
 *****************************************************************************
 * Change Logs:
 * Date           Author       Notes
 * ------------   ----------   -----------------------------------------------
 * 2024-04-05     xqyjlj       initial version
 */
#include "ToolCspRepo.h"
#include "Config.h"
#include "Python.h"
#include "QtJson.h"

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ToolCspRepo::VersionType, Size, Installed, Sha, Urls)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ToolCspRepo::InformationType, Company, Description, Homepage, License, Versions)
} // namespace nlohmann

QT_DEBUG_ADD_TYPE(ToolCspRepo::VersionType)
QT_DEBUG_ADD_TYPE(ToolCspRepo::InformationType)
QT_DEBUG_ADD_TYPE(ToolCspRepo::PackageCellType)
QT_DEBUG_ADD_TYPE(ToolCspRepo::PackageType)

ToolCspRepo::ToolCspRepo() = default;

ToolCspRepo::~ToolCspRepo() = default;

QString ToolCspRepo::dumpPackages(const QString &name)
{
    const QString scriptFile = QString("%1/csp-repo/csp-repo.py").arg(Config::toolsDir());
    const QString data = Python::cmd(scriptFile, { QString("--dump=%1").arg(name),
                                                   QString("--repositories=") + Config::repositoriesDir() });
    return data;
}

void ToolCspRepo::loadPackages(PackageType *packages, const QString &name)
{
    if (packages != nullptr)
    {
        const QString data = dumpPackages(name);
        try
        {
            const std::string buffer = data.toStdString();
            const nlohmann::json json = nlohmann::json::parse(buffer);
            (void)json.get_to(*packages);
        }
        catch (std::exception &e)
        {
            const QString str = QString("try to parse packages failed. \n\nreason: %1").arg(e.what());
            qWarning().noquote() << str;
            packages->clear();
        }
    }
    else
    {
        // TODO: Invalid parameter
    }
}

int ToolCspRepo::installPackage(const QString &name, const QString &version)
{
    PythonAsync *python = PythonAsync::getInstance();
    const QString scriptFile = QString("%1/csp-repo/csp-repo.py").arg(Config::toolsDir());
    const int err = python->execv({ scriptFile, QString("--install=%1").arg(name),
                                    QString("--package-version=%1").arg(version),
                                    QString("--repositories=%1").arg(Config::repositoriesDir()) });
    return err;
}

int ToolCspRepo::updatePackage(const QString &name)
{
    PythonAsync *python = PythonAsync::getInstance();
    const QString scriptFile = QString("%1/csp-repo/csp-repo.py").arg(Config::toolsDir());
    const int err = python->execv({ scriptFile, QString("--update=%1").arg(name),
                                    QString("--repositories=%1").arg(Config::repositoriesDir()) });
    return err;
}

int ToolCspRepo::uninstallPackage(const QString &name, const QString &version)
{
    PythonAsync *python = PythonAsync::getInstance();
    const QString scriptFile = QString("%1/csp-repo/csp-repo.py").arg(Config::toolsDir());
    const int err = python->execv({ scriptFile, QString("--uninstall=%1").arg(name),
                                    QString("--package-version=%1").arg(version),
                                    QString("--repositories=%1").arg(Config::repositoriesDir()) });
    return err;
}
