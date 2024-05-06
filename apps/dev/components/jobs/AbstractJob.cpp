/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        AbstractJob.cpp
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
 *  Copyright (C) 2024-2024 xqyjlj<xqyjlj@126.com>
 *
 * ****************************************************************************
 *  Change Logs:
 *  Date           Author       Notes
 *  ------------   ----------   -----------------------------------------------
 *  2024-04-28     xqyjlj       initial version
 */

#include <QDebug>
#include <QTimer>
#ifdef Q_OS_WIN
#include <windows.h>
#else
#include <signal.h>
#endif

#include "AbstractJob.h"

AbstractJob::AbstractJob(const QString &name)
    : QProcess(nullptr),
      m_item(nullptr),
      m_isStarted(false),
      m_isKilled(false),
      m_title(name),
      m_isNeedFree(true),
      m_startingPercent(0)
{
    setObjectName(name);

    (void)connect(this, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished), this,
                  &AbstractJob::slotSelfFinished);
    (void)connect(this, &AbstractJob::signalProgressUpdated, this, &AbstractJob::slotSelfProgressUpdated);

    m_actionPause = new QAction(tr("Pause This Job"), this);
    m_actions << m_actionPause;
    m_actionResume = new QAction(tr("Resume This Job"), this);
    m_actionResume->setEnabled(false);
    m_actions << m_actionResume;

    (void)connect(m_actionPause, &QAction::triggered, this, &AbstractJob::pause);
    (void)connect(m_actionResume, &QAction::triggered, this, &AbstractJob::resume);
}

AbstractJob::~AbstractJob()
{
    if (m_isNeedFree)
    {
        for (QAction *action : qAsConst(m_actions))
        {
            action->deleteLater();
        }
    }
}

void AbstractJob::setStandardItem(QStandardItem *item)
{
    m_item = item;
}

QStandardItem *AbstractJob::standardItem()
{
    return m_item;
}

bool AbstractJob::isStarted() const
{
    return m_isStarted;
}

bool AbstractJob::isStopped() const
{
    return m_isKilled;
}

void AbstractJob::appendLog(const QString &msg)
{
    if (m_log.size() < 100 * 1024 * 1024 /* MiB */)
    {
        m_log.append(msg);
    }
}

QString AbstractJob::log() const
{
    return m_log;
}

void AbstractJob::setTitle(const QString &title)
{
    m_title = title;
}

QString AbstractJob::title() const
{
    return m_title;
}

bool AbstractJob::paused() const
{
    return !m_actionPause->isEnabled();
}

QList<QAction *> AbstractJob::actions()
{
    m_isNeedFree = false;
    return m_actions;
}

void AbstractJob::start(const QString &program, const QStringList &arguments)
{
    const QString &prog = program;
    const QStringList &args = arguments;
    qDebug().noquote() << prog + " " + arguments.join(" ");
    QProcess::start(prog, args);
    AbstractJob::run();
    m_actionPause->setEnabled(true);
    m_actionResume->setEnabled(false);
}

void AbstractJob::run()
{
    m_isKilled = false;
    m_isStarted = true;
    m_estimateTime.start();
    m_totalTime.start();
    emit signalProgressUpdated(m_item, 0);
}

void AbstractJob::stop()
{
    if (paused())
    {
#ifdef Q_OS_WIN
        ::DebugActiveProcessStop(QProcess::processId());
#else
        ::kill(QProcess::processId(), SIGCONT);
#endif
    }
    closeWriteChannel();
    terminate();
    QTimer::singleShot(2000, this, SLOT(kill()));
    m_isKilled = true;
    m_actionPause->setEnabled(false);
    m_actionResume->setEnabled(false);
}

void AbstractJob::pause()
{
    m_actionPause->setEnabled(false);
    m_actionResume->setEnabled(true);

#ifdef Q_OS_WIN
    ::DebugActiveProcess(QProcess::processId());
#else
    ::kill(QProcess::processId(), SIGSTOP);
#endif
    emit signalProgressUpdated(m_item, -1);
}

void AbstractJob::resume()
{
    m_actionPause->setEnabled(true);
    m_actionResume->setEnabled(false);
    m_startingPercent = -1;
#ifdef Q_OS_WIN
    ::DebugActiveProcessStop(QProcess::processId());
#else
    ::kill(QProcess::processId(), SIGCONT);
#endif
    emit signalProgressUpdated(m_item, 0);
}

// QTime AbstractJob::estimateRemaining(int percent)
// {
//     QTime result;
//     if (percent)
//     {
//         int averageMs = m_estimateTime.elapsed() / qMax(1, percent - qMax(0,
//         m_startingPercent)); result =
//         QTime::fromMSecsSinceStartOfDay(averageMs * (100 - percent));
//     }
//     return result;
// }

void AbstractJob::slotSelfFinished(const int exitCode, const QProcess::ExitStatus exitStatus)
{
    const QTime &time = QTime::fromMSecsSinceStartOfDay(static_cast<int>(m_totalTime.elapsed()));
    if (isOpen())
    {
        m_log.append(readAllStandardOutput());
        m_log.append(readAllStandardError());
    }
    if (exitStatus == QProcess::NormalExit && exitCode == 0 && !m_isKilled)
    {
        qDebug().noquote() << "job successes";
        m_log.append(QString("Completed successfully in %1\n").arg(time.toString()));
        emit signalProgressUpdated(m_item, 100);
        emit signalFinished(this, true);
    }
    else if (m_isKilled)
    {
        qDebug().noquote() << "job stopped";
        m_log.append(QString("Stopped by user at %1\n").arg(time.toString()));
        emit signalFinished(this, false);
    }
    else
    {
        qDebug().noquote() << "job failed with" << exitCode;
        m_log.append(QString("Failed with exit code %1\n").arg(exitCode));
        emit signalFinished(this, false);
    }
}

void AbstractJob::slotSelfProgressUpdated(QStandardItem *item, int percent)
{
    Q_UNUSED(item);
    if (percent > 0 && (percent == 1 || m_startingPercent < 0))
    {
        m_estimateTime.restart();
        m_startingPercent = percent;
    }
}
