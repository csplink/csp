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

static constexpr const char *ConfigKeyRepo = "core/repo";
static constexpr const char *ConfigValueDefaultRepo = "repo";

static constexpr const char *ConfigKeyLanguage = "core/language";
static constexpr const char *ConfigValueDefaultLanguage = "zh_CN";

static constexpr const char *ConfigKeyWorkspace = "core/workspace";
static constexpr const char *ConfigValueDefaultWorkspace = "workspace";

static constexpr const char *ConfigKeyRepositories = "core/repositories";
static constexpr const char *ConfigValueDefaultRepositories = "repositories";

static constexpr const char *ConfigKeyTools = "core/tools";
static constexpr const char *ConfigValueDefaultTools = "tools";

static constexpr const char *ConfigKeyToolXmake = "tools/xmake";
static constexpr const char *ConfigValueDefaultToolXmake = "xmake";

static constexpr const char *ConfigKeyToolGit = "tools/git";
static constexpr const char *ConfigValueDefaultToolGit = "git";

static constexpr const char *ConfigKeyToolPython = "tools/python";
static constexpr const char *ConfigValueDefaultToolPython = "python";

bool Config::isConfig(const QString &key)
{
    return settings_->value(key, ConfigDefaultValue).toString() != ConfigDefaultValue;
}

void Config::init()
{
    settings_ = new QSettings(ConfigFilePath, QSettings::IniFormat);

    if (!isConfig(ConfigKeyRepo))
    {
        settings_->setValue(ConfigKeyRepo, QString("%1/%2").arg(QCoreApplication::applicationDirPath(), ConfigValueDefaultRepo));
    }
    if (!isConfig(ConfigKeyLanguage))
    {
        settings_->setValue(ConfigKeyLanguage, ConfigValueDefaultLanguage);
    }

    if (!isConfig(ConfigKeyRepositories))
    {
        settings_->setValue(ConfigKeyRepositories, QString("%1/%2").arg(QCoreApplication::applicationDirPath(), ConfigValueDefaultRepositories));
    }

    if (!isConfig(ConfigKeyTools))
    {
        settings_->setValue(ConfigKeyTools, QString("%1/%2").arg(QCoreApplication::applicationDirPath(), ConfigValueDefaultTools));
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
    if (!isConfig(ConfigKeyToolPython))
    {
        settings_->setValue(ConfigKeyToolPython, findToolPython());
    }
}

void Config::deinit()
{
    delete settings_;
    settings_ = nullptr;
}

QString Config::get(const QString &key)
{
    QString rtn = ConfigDefaultValue;

    if (settings_ != nullptr)
    {
        rtn = settings_->value(key, ConfigDefaultValue).toString();
    }
    else
    {
        /** TODO: error  */
    }

    return rtn;
}

QString Config::repoDir()
{
    QString rtn = ConfigValueDefaultRepo;

    if (settings_ != nullptr)
    {
        rtn = settings_->value(ConfigKeyRepo, ConfigValueDefaultRepo).toString();
    }
    else
    {
        /** TODO: error  */
    }

    return rtn;
}

void Config::set(const QString &key, const QString &value)
{
    if (settings_ != nullptr)
    {
        settings_->setValue(key, value);
    }
}

QString Config::language()
{
    QString rtn = ConfigValueDefaultLanguage;

    if (settings_ != nullptr)
    {
        rtn = settings_->value(ConfigKeyLanguage, ConfigValueDefaultLanguage).toString();
    }
    else
    {
        /** TODO: error  */
    }

    return rtn;
}

QString Config::workspaceDir()
{
    const QString dir = QString("%1/%2").arg(QCoreApplication::applicationDirPath(), ConfigValueDefaultWorkspace);
    QString rtn = dir;

    if (settings_ != nullptr)
    {
        rtn = settings_->value(ConfigKeyWorkspace, dir).toString();
    }
    else
    {
        /** TODO: error  */
    }

    return rtn;
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
    const QString gitPath = toolGit();
    if (QFile::exists(gitPath))
    {
        const QFileInfo info(gitPath);
        const QString toolDir = QString("%1/..").arg(info.dir().absolutePath());
        envPath = QString("%1/cmd;%2").arg(toolDir, envPath);
        if ("x86_64" == arch)
        {
            envPath = QString("%1;%2/mingw64/bin").arg(envPath, toolDir);
        }
        else if ("i386" == arch)
        {
            envPath = QString("%1;%2/mingw32/bin").arg(envPath, toolDir);
        }
    }
    const QString pythonPath = toolPython();
    if (QFile::exists(pythonPath))
    {
        const QFileInfo info(pythonPath);
        const QString toolDir = info.dir().absolutePath();
        envPath = QString("%1;%2").arg(toolDir, envPath);
        envPath = QString("%1/Scripts;%2").arg(toolDir, envPath);
    }
    map.insert("Path", envPath);
#endif
    map.insert("XMAKE_THEME", "plain");

    return map;
}

QString Config::repositoriesDir()
{
    const QString dir = QString("%1/%2").arg(QCoreApplication::applicationDirPath(), ConfigValueDefaultRepositories);
    QString rtn = dir;

    if (settings_ != nullptr)
    {
        rtn = settings_->value(ConfigKeyRepositories, dir).toString();
    }
    else
    {
        /** TODO: error  */
    }

    return rtn;
}

QString Config::toolsDir()
{
    const QString dir = QString("%1/%2").arg(QCoreApplication::applicationDirPath(), ConfigValueDefaultTools);
    QString rtn = dir;

    if (settings_ != nullptr)
    {
        rtn = settings_->value(ConfigKeyTools, dir).toString();
    }
    else
    {
        /** TODO: error  */
    }

    return rtn;
}

QString Config::toolXmake()
{
    QString rtn = ConfigValueDefaultToolXmake;

    if (settings_ != nullptr)
    {
        rtn = settings_->value(ConfigKeyToolXmake, ConfigValueDefaultToolXmake).toString();
    }
    else
    {
        /** TODO: error  */
    }

    return rtn;
}

QString Config::toolGit()
{
    QString rtn = ConfigValueDefaultToolGit;

    if (settings_ != nullptr)
    {
        rtn = settings_->value(ConfigKeyToolGit, ConfigValueDefaultToolGit).toString();
    }
    else
    {
        /** TODO: error  */
    }

    return rtn;
}

QString Config::toolPython()
{
    QString rtn = ConfigValueDefaultToolPython;

    if (settings_ != nullptr)
    {
        rtn = settings_->value(ConfigKeyToolPython, ConfigValueDefaultToolPython).toString();
    }
    else
    {
        /** TODO: error  */
    }

    return rtn;
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

QString Config::findToolPython()
{
    const QString toolDir = QString("%1/tools").arg(QCoreApplication::applicationDirPath());
#ifdef Q_OS_WINDOWS
    QString pythonPath = QString("%1/python/python.exe").arg(toolDir);
    if (QFile::exists(pythonPath))
    {
        return pythonPath;
    }
#endif
    return ConfigValueDefaultToolPython;
}
