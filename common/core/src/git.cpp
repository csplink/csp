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
#include <QRegularExpression>

#include "git.h"

QString git::version(const QString &program)
{
    QByteArray output;
    QString version = "";

    Q_ASSERT(!program.isEmpty());

    if (os::execv(program, QStringList() << "--version", {}, 1000, "", &output, nullptr))
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

QString git::variables(const int type, const QString &program, const QString &workdir)
{
    QStringList argv;
    QByteArray output;
    QString var = "";

    Q_ASSERT(!program.isEmpty());

    switch (type)
    {
    case TAG:
        argv << "describe"
             << "--tags";
        break;
    case TAG_LONG:
        argv << "describe"
             << "--tags"
             << "--long";
        break;
    case git::BRANCH:
        argv << "rev-parse"
             << "--abbrev-ref"
             << "HEAD";
        break;
    case git::COMMIT:
        argv << "rev-parse"
             << "--short"
             << "HEAD";
        break;
    case COMMIT_LONG:
        argv << "rev-parse"
             << "HEAD";
        break;
    case git::COMMIT_DATE:
        argv << "log"
             << "-1"
             << "--date=format:%Y%m%d%H%M%S"
             << "--format=%ad";
        break;
    default:
        return "";
    }

    if (os::execv(program, argv, {}, 1000, workdir, &output, nullptr))
    {
        var = output.trimmed();
    }
    return var;
}
