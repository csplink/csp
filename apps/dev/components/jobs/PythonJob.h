/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        PythonJob.h
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

#ifndef PYTHON_JOB_H
#define PYTHON_JOB_H

#include <QElapsedTimer>
#include <QProcess>
#include <QString>
#include <QStringList>

class PythonJob : public QProcess
{
    Q_OBJECT
  public:
    explicit PythonJob(QObject *parent = nullptr);
    QString version();

  protected:
    QString cmd(const QStringList &args, const QString &pwd);

  public slots:
    void slotSelfStarted();
    void slotSelfFinished(int exitCode, QProcess::ExitStatus exitStatus);

  private:
    QElapsedTimer m_totalTime;
};

#endif /** PYTHON_JOB_H */
