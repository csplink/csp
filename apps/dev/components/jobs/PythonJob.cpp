/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        PythonJob.cpp
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
 */

#include <QCoreApplication>
#include <QDebug>
#include <QDir>
#include <QRegularExpression>

#include "PythonJob.h"
#include "Settings.h"

PythonJob::PythonJob(const QString &name, const QStringList &args, bool isOpenLog)
    : AbstractJob(name)
{
    if (isOpenLog)
    {
        QAction *action = new QAction(tr("Open Log"), this);
        m_actions << action;
        (void)connect(action, &QAction::triggered, this, &PythonJob::slotActionOpenTriggered);
        (void)connect(this, &QProcess::readyReadStandardOutput, this, &PythonJob::slotSelfReadyReadStandardOutput);
        (void)connect(this, &QProcess::readyReadStandardError, this, &PythonJob::slotSelfReadyReadStandardError);
    }
    m_args.append(args);
}

void PythonJob::start()
{
    AbstractJob::start(Settings.python(), m_args);
}

QString PythonJob::version()
{
    QString version = "not found";

    const QString msg = cmd({"--version"}, QCoreApplication::applicationDirPath());
    static const QRegularExpression regex(R"(Python (\d+\.\d+\.\d+))");
    const QRegularExpressionMatch match = regex.match(msg);

    if (match.hasMatch())
    {
        version = "v" + match.captured(1);
    }

    return version;
}

QString PythonJob::cmd(const QStringList &args, const QString &pwd)
{
    QString value;

    QDir dir(pwd);
    if (dir.exists())
    {
        (void)disconnect(this, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished), this,
                         &AbstractJob::slotSelfFinished);
        (void)disconnect(this, &QProcess::readyReadStandardOutput, this, &PythonJob::slotSelfReadyReadStandardOutput);
        (void)disconnect(this, &QProcess::readyReadStandardError, this, &PythonJob::slotSelfReadyReadStandardError);

        setWorkingDirectory(pwd);
        AbstractJob::start(Settings.python(), args);
        waitForFinished();

        value = readAll().trimmed();

        (void)connect(this, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished), this,
                      &AbstractJob::slotSelfFinished);
        (void)connect(this, &QProcess::readyReadStandardOutput, this, &PythonJob::slotSelfReadyReadStandardOutput);
        (void)connect(this, &QProcess::readyReadStandardError, this, &PythonJob::slotSelfReadyReadStandardError);
    }

    return value;
}

void PythonJob::slotSelfReadyReadStandardOutput()
{
    QString msg;
    do
    {
        msg = readLine();
        appendLog(msg);
    } while (!msg.isEmpty());
}

void PythonJob::slotSelfReadyReadStandardError()
{
    QString msg;
    do
    {
        msg = readLine();
        appendLog(msg);
    } while (!msg.isEmpty());
}

void PythonJob::slotActionOpenTriggered()
{
}
