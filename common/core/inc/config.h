/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        config.h
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

#ifndef COMMON_CORE_CSP_CONFIG_H
#define COMMON_CORE_CSP_CONFIG_H

#include <QSettings>

class config final
{
  public:
    /**
     * @brief check if the key is config
     * @param key: config key
     * @return true if the key is config, otherwise false
     */
    static bool is_config(const QString &key);

    /**
     * @brief init config
     */
    static void init();

    /**
     * @brief deinit config
     */
    static void deinit();

    /**
     * @brief get value by key
     * @param key: config key
     * @return config value
     */
    static QString get(const QString &key);

    /**
     * @brief get csp_repo directory; <get("core/repodir")>
     * @return csp_repo directory; <default: "csp_repo">
     */
    static QString repodir();

    /**
     * @brief get csp_repo directory; <get("core/xmake_repodir")>
     * @return csp_repo directory; <default: "xmake">
     */
    static QString xmake_repodir();

    /**
     * @brief set value by key
     * @param key: config key
     * @param value: config value
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
    static QString workspace();

    /**
     * @brief get default work dir;
     * @return work dir; <always returns a fixed value>
     */
    static QString default_workdir();

    /**
     * @brief get repositories directory; <get("core/repositories")>
     * @return repositories; <default: "repositories">
     */
    static QString repositories();

  private:
    inline static QSettings *_settings = nullptr;

  private:
    config() = default;
    ~config() = default;

    Q_DISABLE_COPY_MOVE(config)
};
#endif //  COMMON_CORE_CSP_CONFIG_H
