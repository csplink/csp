/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        CspRepoJob.cpp
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
 * 2024-04-29     xqyjlj       initial version
 */

#include <QCoreApplication>

#include "CspRepoJob.h"
#include "QtJson.h"
#include "Settings.h"

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(CspRepoJob::VersionType, Size, Installed, Sha, Urls)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(CspRepoJob::InformationType, Company, Description, Homepage, License, Versions)
} // namespace nlohmann

QT_DEBUG_ADD_TYPE(CspRepoJob::VersionType)
QT_DEBUG_ADD_TYPE(CspRepoJob::InformationType)
QT_DEBUG_ADD_TYPE(CspRepoJob::PackageCellType)
QT_DEBUG_ADD_TYPE(CspRepoJob::PackageType)

CspRepoJob::CspRepoJob(const QString &name)
    : PythonJob(name, {}, true)
{
    m_scriptFile = QString("%1/csp-repo/csp-repo.py").arg(Settings.tools());
}

QString CspRepoJob::dumpPackages(const QString &name)
{
    const QStringList args = {
        m_scriptFile,
        QString("--dump=%1").arg(name),
        QString("--repository=") + Settings.repository(),
    };

    return cmd(args, QCoreApplication::applicationDirPath());
}

void CspRepoJob::loadPackages(PackageType *packages, const QString &name)
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

void CspRepoJob::installPackage(const QString &name, const QString &version)
{
    const QStringList args = {
        m_scriptFile,
        QString("--install=%1").arg(name),
        QString("--package-version=%1").arg(version),
        QString("--repository=%1").arg(Settings.repository()),
    };

    setReadChannel(QProcess::StandardOutput);
    AbstractJob::start(Settings.python(), args);
}

void CspRepoJob::updatePackage(const QString &name)
{
    const QStringList args = {
        m_scriptFile,
        QString("--update=%1").arg(name),
        QString("--repository=%1").arg(Settings.repository()),
    };

    setReadChannel(QProcess::StandardOutput);
    AbstractJob::start(Settings.python(), args);
}

void CspRepoJob::uninstallPackage(const QString &name, const QString &version)
{
    const QStringList args = {
        m_scriptFile,
        QString("--uninstall=%1").arg(name),
        QString("--package-version=%1").arg(version),
        QString("--repository=%1").arg(Settings.repository()),
    };

    setReadChannel(QProcess::StandardOutput);
    AbstractJob::start(Settings.python(), args);
}

void CspRepoJob::start()
{
}
