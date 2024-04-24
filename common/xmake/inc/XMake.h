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

#include <QDebug>
#include <QMap>
#include <QObject>
#include <QString>

class XMake final : public QObject
{
    Q_OBJECT

  public:
    static void init();
    static void deinit();

    /**
     * @brief get xmake version
     * @return version; <example: "v2.7.9+HEAD.c879226">
     */
    static QString version();

    static bool execv(const QStringList &argv, QByteArray *output, QByteArray *error);

    static QString cmd(const QString &command, const QStringList &args = {});

    static int build(const QString &path, const QString &mode = "release");

  private:
    XMake();
    ~XMake() override;

    Q_DISABLE_COPY_MOVE(XMake)
};

#endif /** CSP_XMAKE_H */
