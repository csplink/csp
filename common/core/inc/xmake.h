/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        xmake.h
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

#ifndef CSP_COMMON_CORE_XMAKE_H
#define CSP_COMMON_CORE_XMAKE_H

#include <QString>

class xmake final
{
  public:
    typedef struct
    {
        QMap<QString, QString> versions;
        QStringList urls;
        QString homepage;
        QString description;
        QString license;
    } info_t;

    typedef QMap<QString, info_t> package_t;

    typedef struct
    {
        package_t toolchain;
        package_t library;
    } packages_t;

    typedef void (*log_handler)(const QString &msg);

  public:
    /**
     * @brief get xmake version
     * @param program: program path or name
     * @return version; <example: "v2.7.9+HEAD.c879226">
     */
    static QString version(const QString &program = "xmake");

    /**
     * @brief run the lua script.
     * @param lua_path: lua path
     * @param args: args
     * @param program: program path or name
     * @param workdir: working directory
     * @return lua output
     */
    static QString lua(const QString &lua_path, const QStringList &args = {}, const QString &program = "xmake",
                       const QString &workdir = "");

    /**
     * @brief get package configuration from file
     * @param packages: packages ptr
     * @param file: json file path
     * @return void
     */
    static void load_packages_byfile(packages_t *packages, const QString &file);

    /**
     * @brief get package configuration from csp repo
     * @param packages: packages ptr
     * @param program: xmake exe path
     * @param workdir: xmake workdir
     * @return void
     */
    static void load_packages(packages_t *packages, const QString &program = "xmake", const QString &workdir = "");

    static void install_log_handler(log_handler handler);

    static void log(const QString &msg)
    {
        if (_log_handler != nullptr)
        {
            _log_handler(msg);
        }
        else
        {
            qInfo().noquote() << msg;
        }
    }

  private:
    xmake() = default;
    ~xmake() = default;

    inline static log_handler _log_handler = nullptr;

    Q_DISABLE_COPY_MOVE(xmake)
};

#endif //  CSP_COMMON_CORE_XMAKE_H
