/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        Config.cpp
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
#include <QApplication>
#include <QDebug>
#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QMessageBox>
#include <QProcess>
#include <QSysInfo>

#include "Config.h"

static constexpr const char *ConfigFilePath = "config.ini";
static constexpr const char *ConfigDefaultValue = "null";

static constexpr const char *ConfigKeyRepoDir = "core/repoDir";
static constexpr const char *ConfigValueDefaultRepoDir = "repo";

static constexpr const char *ConfigKeyXmakeRepoDir = "core/xmakeRepoDir";
static constexpr const char *ConfigValueDefaultXmakeRepoDir = "xmake";

static constexpr const char *ConfigKeyLanguage = "core/language";
static constexpr const char *ConfigValueDefaultLanguage = "zh_CN";

static constexpr const char *ConfigKeyWorkspace = "core/workspace";
static constexpr const char *ConfigValueDefaultWorkspace = "workspace";

static constexpr const char *ConfigKeyRepositories = "core/repositories";
static constexpr const char *ConfigValueDefaultRepositories = "repositories";

static constexpr const char *ConfigKeyToolXmake = "tool/xmake";
static constexpr const char *ConfigValueDefaultToolXmake = "xmake";

static constexpr const char *ConfigKeyToolGit = "tool/git";
static constexpr const char *ConfigValueDefaultToolGit = "git";

bool Config::is_config(const QString &key)
{
    return _settings->value(key, ConfigDefaultValue).toString() != ConfigDefaultValue;
}

void Config::init()
{
    _settings = new QSettings(ConfigFilePath, QSettings::IniFormat);

    if (!is_config(ConfigKeyRepoDir))
    {
        _settings->setValue(ConfigKeyRepoDir, QString("%1/%2").arg(QCoreApplication::applicationDirPath(), ConfigValueDefaultRepoDir));
    }
    if (!is_config(ConfigKeyXmakeRepoDir))
    {
        _settings->setValue(ConfigKeyXmakeRepoDir, QString("%1/%2").arg(QCoreApplication::applicationDirPath(), ConfigValueDefaultXmakeRepoDir));
    }
    if (!is_config(ConfigKeyLanguage))
    {
        _settings->setValue(ConfigKeyLanguage, ConfigValueDefaultLanguage);
    }

    if (!is_config(ConfigKeyRepositories))
    {
        _settings->setValue(ConfigKeyRepositories, QString("%1/%2").arg(QCoreApplication::applicationDirPath(), ConfigValueDefaultRepositories));
    }

    if (!is_config(ConfigKeyWorkspace))
    {
        const auto appDir = QString("%1/%2").arg(QCoreApplication::applicationDirPath(), ConfigValueDefaultWorkspace);
        const QDir dir(appDir);
        if (!dir.exists())
        {
            if (!dir.mkpath(appDir))
            {
                QMessageBox::critical(nullptr, QObject::tr("Critical"), QObject::tr("The workspace <%1> path is not a directory!").arg(appDir), QMessageBox::Ok);
                QApplication::exit(-1);
            }
        }
        _settings->setValue(ConfigKeyWorkspace, appDir);
    }
    if (!is_config(ConfigKeyToolXmake))
    {
        _settings->setValue(ConfigKeyToolXmake, find_tool_xmake());
    }
    if (!is_config(ConfigKeyToolGit))
    {
        _settings->setValue(ConfigKeyToolGit, find_tool_git());
    }
}

void Config::deinit()
{
    delete _settings;
    _settings = nullptr;
}

QString Config::get(const QString &key)
{
    Q_ASSERT(_settings != nullptr);
    Q_ASSERT(!key.isEmpty());
    return _settings->value(key, ConfigDefaultValue).toString();
}

QString Config::repodir()
{
    Q_ASSERT(_settings != nullptr);
    return _settings->value(ConfigKeyRepoDir, ConfigValueDefaultRepoDir).toString();
}

QString Config::xmake_repodir()
{
    Q_ASSERT(_settings != nullptr);
    return _settings->value(ConfigKeyXmakeRepoDir, ConfigValueDefaultXmakeRepoDir).toString();
}

void Config::set(const QString &key, const QString &value)
{
    Q_ASSERT(_settings != nullptr);
    _settings->setValue(key, value);
}

QString Config::language()
{
    Q_ASSERT(_settings != nullptr);
    return _settings->value(ConfigKeyLanguage, ConfigValueDefaultLanguage).toString();
}

QString Config::workspace_dir()
{
    Q_ASSERT(_settings != nullptr);
    const auto dir = QString("%1/%2").arg(QCoreApplication::applicationDirPath(), ConfigValueDefaultWorkspace);
    return _settings->value(ConfigKeyWorkspace, dir).toString();
}

QString Config::default_workdir()
{
    const QString workDir = QString("%1/workDir").arg(QCoreApplication::applicationDirPath());
    const QString xmakeLua = QString("%1/xmake.lua").arg(workDir);
    const QDir dir(workDir);
    if (!dir.exists())
    {
        (void)dir.mkpath(workDir);
    }

    if (!QFile::exists(xmakeLua))
    {
        QFile file(xmakeLua);
        if (file.open(QIODevice::WriteOnly))
        {
            file.write("");
            file.close();
        }
    }
    return workDir;
}

QMap<QString, QString> Config::env()
{
    QMap<QString, QString> map;
#ifdef Q_OS_WINDOWS
    const QProcessEnvironment environment = QProcessEnvironment::systemEnvironment();
    QString envPath = environment.value("Path");
    const QString arch = QSysInfo::currentCpuArchitecture();
    const QString toolDir = QString("%1/tools").arg(QCoreApplication::applicationDirPath());
    const QString gitPath = QString("%1/git/cmd/git.exe").arg(toolDir);
    if (QFile::exists(gitPath))
    {
        envPath = QString("%1/git/cmd;%2").arg(toolDir, envPath);
        if ("x86_64" == arch)
        {
            envPath = QString("%1;%2/git/mingw64/bin").arg(envPath, toolDir);
        }
        else if ("i386" == arch)
        {
            envPath = QString("%1;%2/git/mingw32/bin").arg(envPath, toolDir);
        }
        map.insert("Path", envPath);
    }
#endif

    map.insert("XMAKE_RCFILES", QString("%1/tools/scripts/xmake.lua").arg(xmake_repodir()));
    map.insert("XMAKE_THEME", "plain");

    return map;
}

QString Config::repositories_dir()
{
    Q_ASSERT(_settings != nullptr);
    const QString dir = QString("%1/%2").arg(QCoreApplication::applicationDirPath(), ConfigValueDefaultRepositories);
    return _settings->value(ConfigKeyRepositories, dir).toString();
}

QString Config::tool_xmake()
{
    Q_ASSERT(_settings != nullptr);
    return _settings->value(ConfigKeyToolXmake, ConfigValueDefaultToolXmake).toString();
}

QString Config::tool_git()
{
    Q_ASSERT(_settings != nullptr);
    return _settings->value(ConfigKeyToolGit, ConfigValueDefaultToolGit).toString();
}

QString Config::find_tool_xmake()
{
    const QString toolDir = QString("%1/tools").arg(QCoreApplication::applicationDirPath());
#ifdef Q_OS_WINDOWS
    QString xmakePath = QString("%1/xmake/xmake.exe").arg(toolDir);
    if (QFile::exists(xmakePath))
    {
        return xmakePath;
    }
#endif

    return ConfigValueDefaultToolXmake;
}

QString Config::find_tool_git()
{
    const QString toolDir = QString("%1/tools").arg(QCoreApplication::applicationDirPath());
#ifdef Q_OS_WINDOWS
    QString gitPath = QString("%1/git/cmd/git.exe").arg(toolDir);
    if (QFile::exists(gitPath))
    {
        return gitPath;
    }
#endif

    return ConfigValueDefaultToolGit;
}
