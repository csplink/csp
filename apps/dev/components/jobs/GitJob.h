/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        GitJob.h
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

#ifndef GIT_JOB_H
#define GIT_JOB_H

#include <QElapsedTimer>
#include <QProcess>
#include <QString>
#include <QStringList>

class GitJob : public QProcess
{
    Q_OBJECT
  public:
    explicit GitJob(QObject *parent = nullptr);

    QString version();
    QString tag(const QString &pwd);
    QString tagLong(const QString &pwd);
    QString branch(const QString &pwd);
    QString commit(const QString &pwd);
    QString commitLong(const QString &pwd);
    QString commitDate(const QString &pwd);

  protected:
    QString cmd(const QStringList &args, const QString &pwd);

  public slots:
    void slotSelfStarted();
    void slotSelfFinished(int exitCode, QProcess::ExitStatus exitStatus);

  private:
    QElapsedTimer m_totalTime;
};

#endif /** GIT_JOB_H */
