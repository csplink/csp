/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        GitJob.cpp
 * @brief
 *
 *****************************************************************************
 * @attention
 * Licensed under the GNU General Public License v. 3 (the "License");
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
 * 2024-04-29     xqyjlj       initial version
 */

#include <QCoreApplication>
#include <QDebug>
#include <QDir>
#include <QRegularExpression>

#include "GitJob.h"
#include "Settings.h"

GitJob::GitJob(const QString &name, const QStringList &args, bool isOpenLog)
    : AbstractJob(name)
{
    if (isOpenLog)
    {
        QAction *action = new QAction(tr("Open Log"), this);
        m_actions << action;
        (void)connect(action, &QAction::triggered, this, &GitJob::slotActionOpenTriggered);
        (void)connect(this, &QProcess::readyReadStandardOutput, this, &GitJob::slotSelfReadyReadStandardOutput);
        (void)connect(this, &QProcess::readyReadStandardError, this, &GitJob::slotSelfReadyReadStandardError);
    }
    m_args.append(args);
}

void GitJob::start()
{
    AbstractJob::start(Settings.python(), m_args);
}

QString GitJob::version()
{
    QString version = "not found";

    const QString msg = cmd({"--version"}, QCoreApplication::applicationDirPath());
    static const QRegularExpression regex(R"(git version (\d+\.\d+\.\d+))");
    const QRegularExpressionMatch match = regex.match(msg);

    if (match.hasMatch())
    {
        version = "v" + match.captured(1);
    }

    return version;
}

QString GitJob::tag(const QString &pwd)
{
    return cmd({"describe", "--tags"}, pwd);
}

QString GitJob::tagLong(const QString &pwd)
{
    return cmd({"describe", "--tags", "--long"}, pwd);
}

QString GitJob::branch(const QString &pwd)
{
    return cmd({"rev-parse", "--abbrev-ref", "HEAD"}, pwd);
}

QString GitJob::commit(const QString &pwd)
{
    return cmd({"rev-parse", "--short", "HEAD"}, pwd);
}

QString GitJob::commitLong(const QString &pwd)
{
    return cmd({"rev-parse", "HEAD"}, pwd);
}

QString GitJob::commitDate(const QString &pwd)
{
    return cmd({"log", "-1", "--date=format:%Y%m%d%H%M%S", "--format=%ad"}, pwd);
}

QString GitJob::cmd(const QStringList &args, const QString &pwd)
{
    QString value;

    QDir dir(pwd);
    if (dir.exists())
    {
        (void)disconnect(this, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished), this,
                         &AbstractJob::slotSelfFinished);
        (void)disconnect(this, &QProcess::readyReadStandardOutput, this, &GitJob::slotSelfReadyReadStandardOutput);
        (void)disconnect(this, &QProcess::readyReadStandardError, this, &GitJob::slotSelfReadyReadStandardError);

        setWorkingDirectory(pwd);
        AbstractJob::start(Settings.git(), args);
        waitForFinished();

        value = readAll().trimmed();

        (void)connect(this, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished), this,
                      &AbstractJob::slotSelfFinished);
        (void)connect(this, &QProcess::readyReadStandardOutput, this, &GitJob::slotSelfReadyReadStandardOutput);
        (void)connect(this, &QProcess::readyReadStandardError, this, &GitJob::slotSelfReadyReadStandardError);
    }

    return value;
}

void GitJob::slotSelfReadyReadStandardOutput()
{
    QString msg;
    do
    {
        msg = readLine();
        appendLog(msg);
    } while (!msg.isEmpty());
}

void GitJob::slotSelfReadyReadStandardError()
{
    QString msg;
    do
    {
        msg = readLine();
        appendLog(msg);
    } while (!msg.isEmpty());
}

void GitJob::slotActionOpenTriggered()
{
}
