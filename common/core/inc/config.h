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

#include <QObject>
#include <QSettings>

class config : public QObject {
    Q_OBJECT

public:
    /**
     * @brief check if the key is config
     * @param key: config key
     * @return true if the key is config, otherwise false
     */
    static bool is_config(const QString &key);

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

private:
    config();
    ~config() override;

    config(const config &signal);
    const config &operator=(const config &signal);

private:
    static config *_instance;
};
#endif  //  COMMON_CORE_CSP_CONFIG_H
