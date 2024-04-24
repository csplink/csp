/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        ToolCspRepo.h
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

#ifndef CSP_TOOL_CSP_REPO_H
#define CSP_TOOL_CSP_REPO_H

#include <QDebug>
#include <QObject>
#include <QString>
#include <QStringList>

class ToolCspRepo final : public QObject
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

    static inline QString dumpPackages(const QString &name = "all");
    static void loadPackages(PackageType *packages, const QString &name = "all");
    static int installPackage(const QString &name, const QString &version);
    static int updatePackage(const QString &name);
    static int uninstallPackage(const QString &name, const QString &version);

  private:
    ToolCspRepo();
    ~ToolCspRepo() override;

    Q_DISABLE_COPY_MOVE(ToolCspRepo)
};

QDebug operator<<(QDebug, const ToolCspRepo::VersionType &);
QDebug operator<<(QDebug, const ToolCspRepo::InformationType &);
QDebug operator<<(QDebug, const ToolCspRepo::PackageCellType &);
QDebug operator<<(QDebug, const ToolCspRepo::PackageType &);

#endif /** CSP_TOOL_CSP_REPO_H */
