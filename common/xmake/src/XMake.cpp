/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        XMake.cpp
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
 *  2023-08-14     xqyjlj       initial version
 */

#include <QDebug>
#include <QFileInfo>
#include <QProcess>
#include <QRegularExpression>

#include "config.h"
#include "os.h"
#include "path.h"
#include "qtjson.h"
#include "XMake.h"

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(XMake::VersionType, Size, Installed, Sha)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(XMake::InformationType, Versions, Urls, Homepage, Description, License, Company)
} // namespace nlohmann

QT_DEBUG_ADD_TYPE(XMake::VersionType)
QT_DEBUG_ADD_TYPE(XMake::InformationType)
QT_DEBUG_ADD_TYPE(XMake::PackageCellType)
QT_DEBUG_ADD_TYPE(XMake::PackageType)

XMake::XMake() = default;

XMake::~XMake() = default;

bool XMake::execv(const QStringList &Argv, QByteArray *Output, QByteArray *Error)
{
    const QString &program = config::tool_xmake();
    const QMap<QString, QString> &env = config::env();
    constexpr int msecs = 30000;
    const QString &workDir = config::default_workdir();
    QProcess process;
    QProcessEnvironment environment = QProcessEnvironment::systemEnvironment();
    bool rtn = false;

    auto envIterator = env.constBegin();
    while (envIterator != env.constEnd())
    {
        environment.insert(envIterator.key(), envIterator.value());
        ++envIterator;
    }

    process.setProgram(program);
    process.setArguments(Argv);
    process.setProcessEnvironment(environment);

    const QFileInfo fileInfo(workDir);
    if (fileInfo.isDir())
    {
        process.setWorkingDirectory(workDir);
    }

    process.start();

    if (process.waitForFinished(msecs))
    {
        rtn = true;
        if (Output != nullptr)
        {
            *Output = process.readAllStandardOutput();
        }
        if (Error != nullptr)
        {
            *Error = process.readAllStandardError();
        }
    }

    return rtn;
}

QString XMake::cmd(const QString &Command, const QStringList &Args)
{
    QByteArray output = "";
    if (!Command.isEmpty())
    {
        QStringList list = { Command, "-D" };
        list << Args;

        (void)execv(list, &output, nullptr);
    }

    return output;
}

QString XMake::version()
{
    QByteArray output;
    QString version;
    QString rtn = "";

    if (execv({ "--version" }, &output, nullptr))
    {
        static const QRegularExpression regex(R"(v(\d+\.\d+\.\d+\+\w+\.\w+))");
        const QRegularExpressionMatch match = regex.match(output);

        if (match.hasMatch())
        {
            rtn = "v" + match.captured(1);
        }
    }

    return rtn;
}

QString XMake::lua(const QString &LuaPath, const QStringList &Args)
{
    QString output = "";
    if (!LuaPath.isEmpty())
    {
        QStringList list = { "-D", path::absolute(LuaPath) };
        list << Args;
        output = cmd("lua", list);
    }

    return output;
}

void XMake::loadPackages(PackageType *Packages)
{
    if (Packages != nullptr)
    {
        const QString data = cmd("csp-repo", { "--dump=json", QString("--repositories=") + config::repositories_dir() });
        try
        {
            const std::string buffer = data.toStdString();
            const nlohmann::json json = nlohmann::json::parse(buffer);
            (void)json.get_to(*Packages);
        }
        catch (std::exception &e)
        {
            const QString str = QString("try to parse packages failed. \n\nreason: %1").arg(e.what());
            qWarning().noquote() << str;
            Packages->clear();
        }
    }
    else
    {
        // TODO: Invalid parameter
    }
}

void XMake::cspCoderLog(const QString &project_file, const QString &output, const QString &repositories)
{
    if (!project_file.isEmpty() && !output.isEmpty() && !repositories.isEmpty())
    {
        cmd("csp-coder", { QString("--project-file=") + project_file, QString("--output=") + output,
                           QString("--repositories=") + repositories });
    }
    else
    {
        // TODO: Invalid parameter
    }
}
