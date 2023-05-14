/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        csp_config.h
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

class csp_config : public QObject {
    Q_OBJECT

public:
    static bool    is_config(const QString &key);
    static QString get(const QString &key);
    static QString repodir();

private:
    csp_config();
    ~csp_config() override;

    csp_config(const csp_config &signal);
    const csp_config &operator=(const csp_config &signal);

private:
    static csp_config *_instance;
};

#endif  //  COMMON_CORE_CSP_CONFIG_H
