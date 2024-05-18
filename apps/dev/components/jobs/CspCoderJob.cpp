/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        CspCoderJob.cpp
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
 * 2024-04-30     xqyjlj       initial version
 */

#include <QDebug>
#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QTime>

#include "CspCoderJob.h"
#include "Settings.h"

CspCoderJob::CspCoderJob(QObject *parent)
    : QProcess(parent)
{
    m_scriptFile = QString("%1/csp-coder/csp-coder.py").arg(Settings.tools());

    (void)connect(this, &QProcess::started, this, &CspCoderJob::slotSelfStarted);
    (void)connect(this, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished), this,
                  &CspCoderJob::slotSelfFinished);
}

void CspCoderJob::generate(const QString &file)
{
    if (QFile::exists(file))
    {
        const QString &prog = Settings.python();
        const QFileInfo info(file);
        const QStringList args = {
            m_scriptFile,
            QString("--file=%1").arg(file),
            QString("--output=%1").arg(info.dir().absolutePath()),
            QString("--repository=%1").arg(Settings.repository()),
        };
        setReadChannel(QProcess::StandardOutput);
        qDebug().noquote() << prog + " " + args.join(" ");
        QProcess::start(prog, args);
    }
    else
    {
        /** TODO: error */
    }
}

void CspCoderJob::slotSelfStarted()
{
    m_totalTime.restart();
}

void CspCoderJob::slotSelfFinished(int exitCode, QProcess::ExitStatus exitStatus)
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
