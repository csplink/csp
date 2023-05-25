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

namespace csp {
class config : public QObject {
    Q_OBJECT

public:
    static bool    is_config(const QString &key);
    static QString get(const QString &key);
    static QString repodir();
    static void    set(const QString &key, const QString &value);
    static QString language();

private:
    config();
    ~config() override;

    config(const config &signal);
    const config &operator=(const config &signal);

private:
    static config *_instance;
};
}  // namespace csp
#endif  //  COMMON_CORE_CSP_CONFIG_H
