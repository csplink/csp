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

#include "config.h"
#include "os.h"
#include "path.h"

#define CSP_CONFIG_FILE_PATH               "config.ini"
#define CSP_CONFIG_DEFAULT_VALUE           "null"

#define CSP_CONFIG_KEY_REPO_DIR            "core/repodir"
#define CSP_CONFIG_VALUE_DEFAULT_REPO_DIR  "csp_repo"

#define CSP_CONFIG_KEY_LANGUAGE            "core/language"
#define CSP_CONFIG_VALUE_DEFAULT_LANGUAGE  "zh_CN"

#define CSP_CONFIG_KEY_WORKSPACE           "core/workspace"
#define CSP_CONFIG_VALUE_DEFAULT_WORKSPACE "workspace"

static QSettings settings(CSP_CONFIG_FILE_PATH, QSettings::IniFormat);

config::config() = default;

config::~config() = default;

bool config::is_config(const QString &key)
{
    return settings.value(key, CSP_CONFIG_DEFAULT_VALUE).toString() != CSP_CONFIG_DEFAULT_VALUE;
}

void config::init()
{
    if (!is_config(CSP_CONFIG_KEY_REPO_DIR))
        settings.setValue(CSP_CONFIG_KEY_REPO_DIR, CSP_CONFIG_VALUE_DEFAULT_REPO_DIR);
    if (!is_config(CSP_CONFIG_KEY_LANGUAGE))
        settings.setValue(CSP_CONFIG_KEY_LANGUAGE, CSP_CONFIG_VALUE_DEFAULT_LANGUAGE);

    if (!is_config(CSP_CONFIG_KEY_WORKSPACE))
    {
        auto appdir = QString("%1/%2").arg(path::appdir(), CSP_CONFIG_VALUE_DEFAULT_WORKSPACE);
        if (!os::exists(appdir))
        {
            os::mkdir(appdir);
        }
        else
        {
            if (!os::isdir(appdir))  // check if it not is a directory
            {
                os::show_error_and_exit(QObject::tr("The workspace <%1> path is not a directory!").arg(appdir));
            }
        }
        settings.setValue(CSP_CONFIG_KEY_WORKSPACE, appdir);
    }
}

QString config::get(const QString &key)
{
    Q_ASSERT(!key.isEmpty());
    return settings.value(key, CSP_CONFIG_DEFAULT_VALUE).toString();
}

QString config::repodir()
{
    return settings.value(CSP_CONFIG_KEY_REPO_DIR, CSP_CONFIG_VALUE_DEFAULT_REPO_DIR).toString();
}

void config::set(const QString &key, const QString &value)
{
    settings.setValue(key, value);
}

QString config::language()
{
    return settings.value(CSP_CONFIG_KEY_LANGUAGE, CSP_CONFIG_VALUE_DEFAULT_LANGUAGE).toString();
}

QString config::workspace()
{
    auto appdir = QString("%1/%2").arg(path::appdir(), CSP_CONFIG_VALUE_DEFAULT_WORKSPACE);
    return settings.value(CSP_CONFIG_KEY_WORKSPACE, appdir).toString();
}
