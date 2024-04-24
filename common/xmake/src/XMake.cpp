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
#include <QDir>
#include <QFileInfo>
#include <QProcess>
#include <QRegularExpression>

#include "Config.h"
#include "XMake.h"
#include "XMakeAsync.h"

XMake::XMake() = default;

XMake::~XMake() = default;

void XMake::init()
{
    XMakeAsync::init();
}

void XMake::deinit()
{
    XMakeAsync::deinit();
}

bool XMake::execv(const QStringList &argv, QByteArray *output, QByteArray *error)
{
    const QString &program = Config::toolXmake();
    const QMap<QString, QString> &env = Config::env();
    constexpr int msecs = 30000;
    const QString &workDir = Config::defaultWorkDir();
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
    process.setArguments(argv);
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
        if (output != nullptr)
        {
            *output = process.readAllStandardOutput();
        }
        if (error != nullptr)
        {
            *error = process.readAllStandardError();
        }
    }

    return rtn;
}

QString XMake::cmd(const QString &command, const QStringList &args)
{
    QByteArray output = "";
    if (!command.isEmpty())
    {
        QStringList list = { command, "-D" };
        list << args;

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

int XMake::build(const QString &path, const QString &mode)
{
    XMakeAsync *xmake = XMakeAsync::getInstance();
    return xmake->build(path, mode);
}
