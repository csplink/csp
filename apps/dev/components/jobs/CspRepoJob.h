/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        CspRepoJob.h
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

#ifndef __CSP_REPO_JOB_H__
#define __CSP_REPO_JOB_H__

#include <QDebug>

#include "PythonJob.h"

class CspRepoJob final : public PythonJob
{
    Q_OBJECT
  public:
    typedef struct
    {
        float Size;
        bool Installed;
        QString Sha;
        QStringList Urls;
    } VersionType;

    typedef struct
    {
        QString Company;
        QString Description;
        QString Homepage;
        QString License;
        QMap<QString, VersionType> Versions;
    } InformationType;

    typedef QMap<QString, InformationType> PackageCellType;
    typedef QMap<QString, PackageCellType> PackageType;

    explicit CspRepoJob(const QString &name);
    QString dumpPackages(const QString &name = "all");
    void loadPackages(PackageType *packages, const QString &name = "all");
    void installPackage(const QString &name, const QString &version);
    void updatePackage(const QString &name);
    void uninstallPackage(const QString &name, const QString &version);

  private:
    QString m_scriptFile;
    void start() override;
};

QDebug operator<<(QDebug, const CspRepoJob::VersionType &);
QDebug operator<<(QDebug, const CspRepoJob::InformationType &);
QDebug operator<<(QDebug, const CspRepoJob::PackageCellType &);
QDebug operator<<(QDebug, const CspRepoJob::PackageType &);

#endif /** __CSP_REPO_JOB_H__ */
