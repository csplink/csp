/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        Settings.cpp
 * @brief
 *
 *****************************************************************************
 * @attention
 * Licensed under the GNU General Public License v. 3 (the "License")
 * You may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.gnu.org/licenses/gpl-3.0.html
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Copyright (C) 2024-2024 xqyjlj<xqyjlj@126.com>
 *
 *****************************************************************************
 * Change Logs:
 * Date           Author       Notes
 * ------------   ----------   -----------------------------------------------
 * 2024-04-27     xqyjlj       initial version
 */

#include <QApplication>
#include <QDebug>
#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QGlobalStatic>
#include <QMessageBox>
#include <QProcess>
#include <QStandardPaths>

#include "Settings.h"

static constexpr const char *SettingsIniFilePath = "/csplink.ini";

static constexpr const char *SettingsKeyLanguage = "language";
static constexpr const char *SettingsKeyDatabase = "database";
static constexpr const char *SettingsKeyWorkspace = "workspace";
static constexpr const char *SettingsKeyRepository = "repository";
static constexpr const char *SettingsKeyTools = "tools";
static constexpr const char *SettingsKeyXmake = "xmake";
static constexpr const char *SettingsKeyGit = "git";
static constexpr const char *SettingsKeyPython = "python";
static constexpr const char *SettingsKeyOpenPath = "openPath";

Q_GLOBAL_STATIC(QScopedPointer<CspSettings>, instance)

CspSettings::CspSettings()
    : QObject(),
      m_settings(QCoreApplication::applicationDirPath() + SettingsIniFilePath, QSettings::IniFormat)
{
}

CspSettings &CspSettings::singleton()
{
    if (!*instance)
    {
        instance->reset(new CspSettings());
    }
    return **instance;
}

void CspSettings::checkDirValid(const char *key, const QString &dir, const bool create)
{
    bool isValid = true;
    const QDir dirInfo(dir);

    if (!dirInfo.exists())
    {
        isValid = false;
        if (create)
        {
            if (dirInfo.mkpath(dir))
            {
                isValid = true;
            }
        }
    }

    if (!isValid)
    {
        QMessageBox::critical(nullptr, tr("Critical"), tr("The '%1' <%2> path is not a directory!").arg(key, dir),
                              QMessageBox::Ok);
        QApplication::exit(-1);
    }
}

/** get the display language */
QString CspSettings::language() const
{
    QString language = m_settings.value(SettingsKeyLanguage, QLocale().name()).toString();
    if (language == "en")
    {
        language = "en_US";
    }
    return language;
}

/** set the display language */
void CspSettings::setLanguage(const QString &language)
{
    m_settings.setValue(SettingsKeyLanguage, language);
}

/** get the database directory */
QString CspSettings::database() const
{
    QString database;

    database = m_settings.value(SettingsKeyDatabase, QCoreApplication::applicationDirPath() + "/database").toString();

    checkDirValid(SettingsKeyDatabase, database, false);

    return database;
}

/** set the database directory */
void CspSettings::setDatabase(const QString &database)
{
    m_settings.setValue(SettingsKeyDatabase, database);
}

QString CspSettings::workspace() const
{
    QString workspace;

    workspace =
        m_settings.value(SettingsKeyWorkspace, QCoreApplication::applicationDirPath() + "/workspace").toString();

    checkDirValid(SettingsKeyWorkspace, workspace, true);

    return workspace;
}

void CspSettings::setWorkspace(const QString &workspace)
{
    m_settings.setValue(SettingsKeyWorkspace, workspace);
}

QString CspSettings::repository() const
{
    QString repository;

    repository =
        m_settings.value(SettingsKeyRepository, QCoreApplication::applicationDirPath() + "/repository").toString();

    checkDirValid(SettingsKeyRepository, repository, true);

    return repository;
}

void CspSettings::setRepository(const QString &repository)
{
    m_settings.setValue(SettingsKeyRepository, repository);
}

QString CspSettings::tools() const
{
    QString tools;

    tools = m_settings.value(SettingsKeyTools, QCoreApplication::applicationDirPath() + "/tools").toString();

    checkDirValid(SettingsKeyTools, tools, false);

    return tools;
}

void CspSettings::setTools(const QString &tools)
{
    m_settings.setValue(SettingsKeyTools, tools);
}

QString CspSettings::xmake() const
{
    QString xmake;
    QString xmakeDefaultPath = "xmake";

#if defined(Q_OS_WINDOWS)
    QString xmakePath = QString("%1/xmake/xmake.exe").arg(tools());
    if (QFile::exists(xmakePath))
    {
        xmakeDefaultPath = xmakePath;
    }
#endif /** defined(Q_OS_WINDOWS) */

    xmake = m_settings.value(SettingsKeyXmake, xmakeDefaultPath).toString();

    return xmake;
}

void CspSettings::setXmake(const QString &xmake)
{
    m_settings.setValue(SettingsKeyXmake, xmake);
}

QString CspSettings::git() const
{
    QString git;
    QString gitDefaultPath = "git";

#if defined(Q_OS_WINDOWS)
    QString gitPath = QString("%1/git/cmd/git.exe").arg(tools());
    if (QFile::exists(gitPath))
    {
        gitDefaultPath = gitPath;
    }
#endif /** defined(Q_OS_WINDOWS) */

    git = m_settings.value(SettingsKeyGit, gitDefaultPath).toString();

    return git;
}

void CspSettings::setGit(const QString &git)
{
    m_settings.setValue(SettingsKeyGit, git);
}

QString CspSettings::python() const
{
    QString python;
    QString pythonDefaultPath = "python";

#if defined(Q_OS_WINDOWS)
    QString pythonPath = QString("%1/python/python.exe").arg(tools());
    if (QFile::exists(pythonPath))
    {
        pythonDefaultPath = pythonPath;
    }
#endif /** defined(Q_OS_WINDOWS) */

    python = m_settings.value(SettingsKeyPython, pythonDefaultPath).toString();

    return python;
}

void CspSettings::setPython(const QString &python)
{
    m_settings.setValue(SettingsKeyPython, python);
}

QString CspSettings::openPath() const
{
    const QStringList locations = QStandardPaths::standardLocations(QStandardPaths::DocumentsLocation);
    QString defaultValue = "";
    if (!locations.isEmpty())
    {
        defaultValue = locations[0];
    }
    return m_settings.value(SettingsKeyOpenPath, defaultValue).toString();
}

void CspSettings::setOpenPath(const QString &path)
{
    m_settings.setValue(SettingsKeyOpenPath, path);
}

QMap<QString, QString> CspSettings::env() const
{
    QMap<QString, QString> env;

#if defined(Q_OS_WINDOWS)
    const QProcessEnvironment environment = QProcessEnvironment::systemEnvironment();
    QString envPath = environment.value("Path");
    const QString arch = QSysInfo::currentCpuArchitecture();
    const QString gitPath = git();

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

    const QString pythonPath = python();
    if (QFile::exists(pythonPath))
    {
        const QFileInfo info(pythonPath);
        const QString toolDir = info.dir().absolutePath();
        envPath = QString("%1;%2").arg(toolDir, envPath);
        envPath = QString("%1/Scripts;%2").arg(toolDir, envPath);
    }

    env.insert("Path", envPath);
#endif /** defined(Q_OS_WINDOWS) */

    env.insert("XMAKE_THEME", "plain");

    return env;
}
