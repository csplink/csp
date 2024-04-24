/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        Config.h
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
 *  2023-05-14     xqyjlj       initial version
 */

#ifndef CSP_CONFIG_H
#define CSP_CONFIG_H

#include <QSettings>

class Config final
{
  public:
    /**
     * @brief check if the key is Config
     * @param key: Config key
     * @return true if the key is Config, otherwise false
     */
    static bool isConfig(const QString &key);

    /**
     * @brief init Config
     */
    static void init();

    /**
     * @brief deinit Config
     */
    static void deinit();

    /**
     * @brief get value by key
     * @param key: Config key
     * @return Config value
     */
    static QString get(const QString &key);

    /**
     * @brief get csp_repo directory; <get("core/repo")>
     * @return csp_repo directory; <default: "csp_repo">
     */
    static QString repoDir();

    /**
     * @brief set value by key
     * @param key: Config key
     * @param value: Config value
     */
    static void set(const QString &key, const QString &value);

    /**
     * @brief get csp_repo directory; <get("core/language")>
     * @return language; <default: "zh_CN">
     */
    static QString language();

    /**
     * @brief get workspace directory; <get("core/workspace")>
     * @return workspace; <default: "workspace">
     */
    static QString workspaceDir();

    /**
     * @brief get default work dir;
     * @return work dir; <always returns a fixed value>
     */
    static QString defaultWorkDir();

    /**
     * @brief get work env
     * @return env map
     */
    static QMap<QString, QString> env();

    /**
     * @brief get repositories directory; <get("core/repositories")>
     * @return repositories; <default: "repositories">
     */
    static QString repositoriesDir();

    static QString toolsDir();

    static QString toolXmake();

    static QString toolGit();

    static QString toolPython();

  private:
    inline static QSettings *settings_ = nullptr;

    static QString findToolXmake();
    static QString findToolGit();
    static QString findToolPython();

    Config() = default;
    ~Config() = default;

    Q_DISABLE_COPY_MOVE(Config)
};
#endif /** CSP_CONFIG_H */
