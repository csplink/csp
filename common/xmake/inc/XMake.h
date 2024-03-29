/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        XMake.h
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
 *  2023-08-14     xqyjlj       initial version
 */

#ifndef CSP_XMAKE_H
#define CSP_XMAKE_H

#include <QMap>
#include <QObject>
#include <QString>

class XMake final : public QObject
{
    Q_OBJECT

  public:
    typedef struct
    {
        float Size;
        bool Installed;
        QString Sha;
    } VersionType;

    typedef struct
    {
        QMap<QString, VersionType> Versions;
        QStringList Urls;
        QString Homepage;
        QString Description;
        QString License;
        QString Company;
    } InformationType;

    typedef QMap<QString, InformationType> PackageCellType;
    typedef QMap<QString, PackageCellType> PackageType;

    /**
     * @brief get xmake version
     * @return version; <example: "v2.7.9+HEAD.c879226">
     */
    static QString version();

    static bool execv(const QStringList &argv, QByteArray *output, QByteArray *error);

    static QString cmd(const QString &command, const QStringList &args = {});

    /**
     * @brief run the lua script.
     * @param luaPath: lua path
     * @param args: args
     * @return lua output
     */
    static QString lua(const QString &luaPath, const QStringList &args = {});

    /**
     * @brief get package configuration from csp repo
     * @param packages: packages ptr
     * @param name: packages name
     * @return void
     */
    static void loadPackages(PackageType *packages, const QString &name = "");

  private:
    XMake();
    ~XMake() override;

    Q_DISABLE_COPY_MOVE(XMake)
};

QDebug operator<<(QDebug, const XMake::VersionType &);
QDebug operator<<(QDebug, const XMake::InformationType &);
QDebug operator<<(QDebug, const XMake::PackageCellType &);
QDebug operator<<(QDebug, const XMake::PackageType &);

#endif /** CSP_XMAKE_H */
