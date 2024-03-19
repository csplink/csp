/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        git.cpp
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

#include "Git.h"

bool Git::execv(const QStringList &Argv, QByteArray *Output, QByteArray *Error, const QString &WorkDir)
{
    const QString &program = Config::tool_git();
    const QMap<QString, QString> &env = Config::env();
    constexpr int msecs = 30000;
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

    const QFileInfo fileInfo(WorkDir);
    if (fileInfo.isDir())
    {
        process.setWorkingDirectory(WorkDir);
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

QString Git::version(void)
{
    QByteArray output;
    QString version = "";

    if (execv({ "--version" }, &output, nullptr))
    {
        const QRegularExpression regex(R"(git version (\d+\.\d+\.\d+))");
        const QRegularExpressionMatch match = regex.match(output);

        if (match.hasMatch())
        {
            version = "v" + match.captured(1);
        }
    }
    return version;
}

QString Git::variables(const int Type, const QString &WorkDir)
{
    QStringList argv;
    QByteArray output;
    QString var = "";

    switch (Type)
    {
    case TAG:
        argv = QStringList({ "describe", "--tags" });
        break;
    case TAG_LONG:
        argv = QStringList({ "describe", "--tags", "--long" });
        break;
    case BRANCH:
        argv = QStringList({ "rev-parse", "--abbrev-ref", "HEAD" });
        break;
    case COMMIT:
        argv = QStringList({ "rev-parse", "--short", "HEAD" });
        break;
    case COMMIT_LONG:
        argv = QStringList({ "rev-parse", "HEAD" });
        break;
    case COMMIT_DATE:
        argv = QStringList({ "log", "-1", "--date=format:%Y%m%d%H%M%S", "--format=%ad" });
        break;
    default:
        return "";
    }

    if (execv(argv, &output, nullptr, WorkDir))
    {
        var = output.trimmed();
    }
    return var;
}
