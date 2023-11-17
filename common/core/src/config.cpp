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

bool config::is_config(const QString &key)
{
    return _settings->value(key, CSP_CONFIG_DEFAULT_VALUE).toString() != CSP_CONFIG_DEFAULT_VALUE;
}

void config::init()
{
    _settings = new QSettings(CSP_CONFIG_FILE_PATH, QSettings::IniFormat);

    if (!is_config(CSP_CONFIG_KEY_REPO_DIR))
        _settings->setValue(CSP_CONFIG_KEY_REPO_DIR, CSP_CONFIG_VALUE_DEFAULT_REPO_DIR);
    if (!is_config(CSP_CONFIG_KEY_LANGUAGE))
        _settings->setValue(CSP_CONFIG_KEY_LANGUAGE, CSP_CONFIG_VALUE_DEFAULT_LANGUAGE);

    if (!is_config(CSP_CONFIG_KEY_WORKSPACE))
    {
        const auto appdir = QString("%1/%2").arg(path::appdir(), CSP_CONFIG_VALUE_DEFAULT_WORKSPACE);
        if (!os::exists(appdir))
        {
            os::mkdir(appdir);
        }
        else
        {
            if (!os::isdir(appdir)) // check if it not is a directory
            {
                os::show_error_and_exit(QObject::tr("The workspace <%1> path is not a directory!").arg(appdir));
            }
        }
        _settings->setValue(CSP_CONFIG_KEY_WORKSPACE, appdir);
    }
}

void config::deinit()
{
    delete _settings;
    _settings = nullptr;
}

QString config::get(const QString &key)
{
    Q_ASSERT(_settings != nullptr);
    Q_ASSERT(!key.isEmpty());
    return _settings->value(key, CSP_CONFIG_DEFAULT_VALUE).toString();
}

QString config::repodir()
{
    Q_ASSERT(_settings != nullptr);
    return _settings->value(CSP_CONFIG_KEY_REPO_DIR, CSP_CONFIG_VALUE_DEFAULT_REPO_DIR).toString();
}

void config::set(const QString &key, const QString &value)
{
    Q_ASSERT(_settings != nullptr);
    _settings->setValue(key, value);
}

QString config::language()
{
    Q_ASSERT(_settings != nullptr);
    return _settings->value(CSP_CONFIG_KEY_LANGUAGE, CSP_CONFIG_VALUE_DEFAULT_LANGUAGE).toString();
}

QString config::workspace()
{
    Q_ASSERT(_settings != nullptr);
    const auto appdir = QString("%1/%2").arg(path::appdir(), CSP_CONFIG_VALUE_DEFAULT_WORKSPACE);
    return _settings->value(CSP_CONFIG_KEY_WORKSPACE, appdir).toString();
}
