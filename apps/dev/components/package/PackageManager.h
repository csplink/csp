/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        PackageManager.h
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
 *  Copyright (C) 2024-2024 xqyjlj<xqyjlj@126.com>
 *
 * ****************************************************************************
 *  Change Logs:
 *  Date           Author       Notes
 *  ------------   ----------   -----------------------------------------------
 *  2024-06-08     xqyjlj       initial version
 */

#ifndef PACKAGE_MANAGER_H
#define PACKAGE_MANAGER_H

#include <QDebug>
#include <QMap>
#include <QObject>
#include <QStringList>

class CspPackageManager final : public QObject
{
    Q_OBJECT
  public:
    typedef struct
    {
        QString Path;
    } PackageType;

    typedef QMap<QString, PackageType> PackageVersionType;
    typedef QMap<QString, PackageVersionType> PackagesType;

    explicit CspPackageManager();
    static CspPackageManager &singleton();

    static bool loadPackages(PackagesType *packages, const QString &path);

    void uninstall(const QString &name, const QString &version);
    void install(const QString &path);
    void installAsync(const QString &path);
    QStringList packages();
    QStringList packageVersions(const QString &name);
    bool packageInstalled(const QString &name, const QString &version);
    QString packagePath(const QString &name, const QString &version);

  private:
    PackagesType m_packages;

    bool unzip(const QString &path);
    bool install();

    Q_DISABLE_COPY_MOVE(CspPackageManager)
};

#define PackageManager CspPackageManager::singleton()

QDebug operator<<(QDebug, const CspPackageManager::PackageType &);
QDebug operator<<(QDebug, const CspPackageManager::PackageVersionType &);
QDebug operator<<(QDebug, const CspPackageManager::PackagesType &);

#endif /** PACKAGE_MANAGER_H */
