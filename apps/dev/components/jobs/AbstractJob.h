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
    ~AbstractJob() override;

    void setStandardItem(QStandardItem *item);
    QStandardItem *standardItem();
    bool isStarted() const;
    bool isStopped() const;
    void appendLog(const QString &msg);
    QString log() const;
    void setTitle(const QString &title);
    QString title() const;
    bool paused() const;
    QList<QAction *> actions();

  public slots:
    void start(const QString &program, const QStringList &arguments);
    virtual void run();
    virtual void stop();
    void pause();
    void resume();
    void slotSelfFinished(int exitCode, QProcess::ExitStatus exitStatus);

  signals:
    void signalProgressUpdated(QStandardItem *item, int percent);
    void signalFinished(AbstractJob *job, bool isSuccess, QString failureTime = QString());

  protected:
    QList<QAction *> m_actions;
    QStandardItem *m_item;

  private slots:
    void slotSelfProgressUpdated(QStandardItem *item, int percent);

  private:
    bool m_isStarted;
    bool m_isKilled;
    QString m_log;
    QString m_title;
    bool m_isNeedFree;
    QElapsedTimer m_estimateTime;
    int m_startingPercent;
    QElapsedTimer m_totalTime;
    QAction *m_actionPause;
    QAction *m_actionResume;
};

#endif /** __ABSTRACT_JOB_H__ */
