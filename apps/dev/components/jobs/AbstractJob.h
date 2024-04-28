/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        AbstractJob.h
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

#ifndef __ABSTRACT_JOB_H__
#define __ABSTRACT_JOB_H__

#include <QAction>
#include <QElapsedTimer>
#include <QList>
#include <QModelIndex>
#include <QProcess>
#include <QStandardItem>
#include <QTime>

class AbstractJob : public QProcess
{
    Q_OBJECT
  public:
    explicit AbstractJob(const QString &name);
    virtual ~AbstractJob();

    void setStandardItem(QStandardItem *item);
    QStandardItem *standardItem(void);
    bool isDone() const;
    bool isStopped() const;
    void appendLog(const QString &msg);
    QString log() const;
    void setTitle(const QString &title);
    QString title() const;
    bool paused() const;
    QList<QAction *> actions() const;

  public slots:
    void start(const QString &program, const QStringList &arguments);
    virtual void run();
    virtual void stop();
    void pause();
    void resume();

  signals:
    void signalProgressUpdated(QStandardItem *item, int percent);
    void finished(AbstractJob *job, bool isSuccess, QString failureTime = QString());

  protected:
    QList<QAction *> m_actions;
    QStandardItem *m_item;

  protected slots:
    virtual void selfFinishedCallback(int exitCode, QProcess::ExitStatus exitStatus);
    virtual void selfReadyReadCallback();
    virtual void selfStartedCallback();

  private slots:
    void selfProgressUpdatedCallback(QStandardItem *item, int percent);

  private:
    bool m_isDone;
    bool m_isKilled;
    QString m_log;
    QString m_title;
    QElapsedTimer m_estimateTime;
    int m_startingPercent;
    QElapsedTimer m_totalTime;
    // QScopedPointer<PostJobAction> m_postJobAction;
    QAction *m_actionPause;
    QAction *m_actionResume;
};

#endif /** __ABSTRACT_JOB_H__ */
