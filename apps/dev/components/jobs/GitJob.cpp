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
#include <QTime>

#include "GitJob.h"
#include "Settings.h"

GitJob::GitJob(QObject *parent)
    : QProcess(parent)
{
    (void)connect(this, &QProcess::started, this, &GitJob::slotSelfStarted);
    (void)connect(this, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished), this, &GitJob::slotSelfFinished);
}

QString GitJob::version()
{
    QString version = "";

    setReadChannel(QProcess::StandardOutput);
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
    setReadChannel(QProcess::StandardOutput);
    return cmd({"describe", "--tags"}, pwd);
}

QString GitJob::tagLong(const QString &pwd)
{
    setReadChannel(QProcess::StandardOutput);
    return cmd({"describe", "--tags", "--long"}, pwd);
}

QString GitJob::branch(const QString &pwd)
{
    setReadChannel(QProcess::StandardOutput);
    return cmd({"rev-parse", "--abbrev-ref", "HEAD"}, pwd);
}

QString GitJob::commit(const QString &pwd)
{
    setReadChannel(QProcess::StandardOutput);
    return cmd({"rev-parse", "--short", "HEAD"}, pwd);
}

QString GitJob::commitLong(const QString &pwd)
{
    setReadChannel(QProcess::StandardOutput);
    return cmd({"rev-parse", "HEAD"}, pwd);
}

QString GitJob::commitDate(const QString &pwd)
{
    setReadChannel(QProcess::StandardOutput);
    return cmd({"log", "-1", "--date=format:%Y%m%d%H%M%S", "--format=%ad"}, pwd);
}

QString GitJob::cmd(const QStringList &args, const QString &pwd)
{
    QString value;

    QDir dir(pwd);
    if (dir.exists())
    {
        const QString &prog = Settings.git();
        setWorkingDirectory(pwd);
        qDebug().noquote() << prog + " " + args.join(" ");

        (void)disconnect(this, &QProcess::started, this, &GitJob::slotSelfStarted);
        (void)disconnect(this, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished), this,
                         &GitJob::slotSelfFinished);

        QProcess::start(prog, args);
        waitForFinished();

        (void)connect(this, &QProcess::started, this, &GitJob::slotSelfStarted);
        (void)connect(this, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished), this,
                      &GitJob::slotSelfFinished);

        value = readAll().trimmed();
        qDebug().noquote() << value;
    }

    return value;
}

void GitJob::slotSelfStarted()
{
    m_totalTime.restart();
}

void GitJob::slotSelfFinished(int exitCode, QProcess::ExitStatus exitStatus)
{
    const QTime &time = QTime::fromMSecsSinceStartOfDay(static_cast<int>(m_totalTime.elapsed()));

    if (exitStatus == QProcess::NormalExit && exitCode == 0)
    {
        qDebug().noquote() << "job successes";
        qDebug().noquote() << QString("Completed successfully in %1\n").arg(time.toString());
    }
    else
    {
        qDebug().noquote() << "job failed with" << exitCode;
    }
}
