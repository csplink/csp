/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        xmake.cpp
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

#include "path.h"
#include "xmake.h"

QString xmake::version(const QString &program)
{
    QByteArray output;
    QString version = "";

    Q_ASSERT(!program.isEmpty());

    if (os::execv(program, QStringList() << "--version", {}, 1000, "", &output, nullptr))
    {
        const QRegularExpression regex(R"(v(\d+\.\d+\.\d+\+\w+\.\w+))");
        const QRegularExpressionMatch match = regex.match(output);

        if (match.hasMatch())
        {
            version = "v" + match.captured(1);
        }
    }
    return version;
}

QString xmake::lua(const QString &p, const QString &program, const QString &workdir)
{
    QByteArray output;

    Q_ASSERT(!p.isEmpty());
    Q_ASSERT(!program.isEmpty());

    if (os::execv(program, QStringList() << "lua" << path::absolute(p), {}, 1000, workdir, &output, nullptr))
    {
    }

    return output;
}
