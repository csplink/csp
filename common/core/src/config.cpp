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

static constexpr const char *csp_config_file_path = "config.ini";
static constexpr const char *csp_config_default_value = "null";

static constexpr const char *csp_config_key_repo_dir = "core/repodir";
static constexpr const char *csp_config_value_default_repo_dir = "csp_repo";

static constexpr const char *csp_config_key_language = "core/language";
static constexpr const char *csp_config_value_default_language = "zh_CN";

static constexpr const char *csp_config_key_workspace = "core/workspace";
static constexpr const char *csp_config_value_default_workspace = "workspace";

bool config::is_config(const QString &key)
{
    return _settings->value(key, csp_config_default_value).toString() != csp_config_default_value;
}

void config::init()
{
    _settings = new QSettings(csp_config_file_path, QSettings::IniFormat);

    if (!is_config(csp_config_key_repo_dir))
        _settings->setValue(csp_config_key_repo_dir, csp_config_value_default_repo_dir);
    if (!is_config(csp_config_key_language))
        _settings->setValue(csp_config_key_language, csp_config_value_default_language);

    if (!is_config(csp_config_key_workspace))
    {
        const auto appdir = QString("%1/%2").arg(path::appdir(), csp_config_value_default_workspace);
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
        _settings->setValue(csp_config_key_workspace, appdir);
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
    return _settings->value(key, csp_config_default_value).toString();
}

QString config::repodir()
{
    Q_ASSERT(_settings != nullptr);
    return _settings->value(csp_config_key_repo_dir, csp_config_value_default_repo_dir).toString();
}

void config::set(const QString &key, const QString &value)
{
    Q_ASSERT(_settings != nullptr);
    _settings->setValue(key, value);
}

QString config::language()
{
    Q_ASSERT(_settings != nullptr);
    return _settings->value(csp_config_key_language, csp_config_value_default_language).toString();
}

QString config::workspace()
{
    Q_ASSERT(_settings != nullptr);
    const auto appdir = QString("%1/%2").arg(path::appdir(), csp_config_value_default_workspace);
    return _settings->value(csp_config_key_workspace, appdir).toString();
}
