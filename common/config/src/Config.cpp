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

bool Config::isConfig(const QString &key)
{
    return settings_->value(key, ConfigDefaultValue).toString() != ConfigDefaultValue;
}

void Config::init()
{
    settings_ = new QSettings(ConfigFilePath, QSettings::IniFormat);

    if (!isConfig(ConfigKeyRepoDir))
    {
        settings_->setValue(ConfigKeyRepoDir, QString("%1/%2").arg(QCoreApplication::applicationDirPath(), ConfigValueDefaultRepoDir));
    }
    if (!isConfig(ConfigKeyXmakeRepoDir))
    {
        settings_->setValue(ConfigKeyXmakeRepoDir, QString("%1/%2").arg(QCoreApplication::applicationDirPath(), ConfigValueDefaultXmakeRepoDir));
    }
    if (!isConfig(ConfigKeyLanguage))
    {
        settings_->setValue(ConfigKeyLanguage, ConfigValueDefaultLanguage);
    }

    if (!isConfig(ConfigKeyRepositories))
    {
        settings_->setValue(ConfigKeyRepositories, QString("%1/%2").arg(QCoreApplication::applicationDirPath(), ConfigValueDefaultRepositories));
    }

    if (!isConfig(ConfigKeyWorkspace))
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
        settings_->setValue(ConfigKeyWorkspace, appDir);
    }
    if (!isConfig(ConfigKeyToolXmake))
    {
        settings_->setValue(ConfigKeyToolXmake, findToolXmake());
    }
    if (!isConfig(ConfigKeyToolGit))
    {
        settings_->setValue(ConfigKeyToolGit, findToolGit());
    }
}

void Config::deinit()
{
    delete settings_;
    settings_ = nullptr;
}

QString Config::get(const QString &key)
{
    Q_ASSERT(settings_ != nullptr);
    Q_ASSERT(!key.isEmpty());
    return settings_->value(key, ConfigDefaultValue).toString();
}

QString Config::repoDir()
{
    Q_ASSERT(settings_ != nullptr);
    return settings_->value(ConfigKeyRepoDir, ConfigValueDefaultRepoDir).toString();
}

QString Config::xmakeRepoDir()
{
    Q_ASSERT(settings_ != nullptr);
    return settings_->value(ConfigKeyXmakeRepoDir, ConfigValueDefaultXmakeRepoDir).toString();
}

void Config::set(const QString &key, const QString &value)
{
    Q_ASSERT(settings_ != nullptr);
    settings_->setValue(key, value);
}

QString Config::language()
{
    Q_ASSERT(settings_ != nullptr);
    return settings_->value(ConfigKeyLanguage, ConfigValueDefaultLanguage).toString();
}

QString Config::workspaceDir()
{
    Q_ASSERT(settings_ != nullptr);
    const auto dir = QString("%1/%2").arg(QCoreApplication::applicationDirPath(), ConfigValueDefaultWorkspace);
    return settings_->value(ConfigKeyWorkspace, dir).toString();
}

QString Config::defaultWorkDir()
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

    map.insert("XMAKE_RCFILES", QString("%1/tools/scripts/xmake.lua").arg(xmakeRepoDir()));
    map.insert("XMAKE_THEME", "plain");

    return map;
}

QString Config::repositoriesDir()
{
    Q_ASSERT(settings_ != nullptr);
    const QString dir = QString("%1/%2").arg(QCoreApplication::applicationDirPath(), ConfigValueDefaultRepositories);
    return settings_->value(ConfigKeyRepositories, dir).toString();
}

QString Config::toolXmake()
{
    Q_ASSERT(settings_ != nullptr);
    return settings_->value(ConfigKeyToolXmake, ConfigValueDefaultToolXmake).toString();
}

QString Config::toolGit()
{
    Q_ASSERT(settings_ != nullptr);
    return settings_->value(ConfigKeyToolGit, ConfigValueDefaultToolGit).toString();
}

QString Config::findToolXmake()
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

QString Config::findToolGit()
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
