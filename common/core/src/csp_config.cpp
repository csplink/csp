/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        csp_config.cpp
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
#include <QFile>

#include "csp_config.h"

#define CSP_CONFIG_FILE_PATH              "config.ini"
#define CSP_CONFIG_DEFAULT_VALUE          "null"

#define CSP_CONFIG_KEY_REPO_DIR           "core/repodir"
#define CSP_CONFIG_VALUE_DEFAULT_REPO_DIR "csp_repo"

static QSettings _settings(CSP_CONFIG_FILE_PATH, QSettings::IniFormat);

csp_config *csp_config::_instance = new csp_config();

csp_config::csp_config()
{
    if (!is_config(CSP_CONFIG_KEY_REPO_DIR))
        _settings.setValue(CSP_CONFIG_KEY_REPO_DIR, CSP_CONFIG_VALUE_DEFAULT_REPO_DIR);
}

csp_config::~csp_config() = default;

bool csp_config::is_config(const QString &key)
{
    return _settings.value(key, CSP_CONFIG_DEFAULT_VALUE).toString() != CSP_CONFIG_DEFAULT_VALUE;
}

QString csp_config::get(const QString &key)
{
    Q_ASSERT(!key.isEmpty());
    return _settings.value(key, CSP_CONFIG_DEFAULT_VALUE).toString();
}

QString csp_config::repodir()
{
    return _settings.value(CSP_CONFIG_KEY_REPO_DIR, CSP_CONFIG_VALUE_DEFAULT_REPO_DIR).toString();
}
