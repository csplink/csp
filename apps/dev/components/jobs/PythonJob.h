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

#ifndef __PYTHON_JOB_H__
#define __PYTHON_JOB_H__

#include <QString>
#include <QStringList>

#include "AbstractJob.h"

class PythonJob : public AbstractJob
{
    Q_OBJECT
  public:
    explicit PythonJob(const QString &name, const QStringList &args, bool isOpenLog = false);
    virtual void start();
    QString version();

  protected:
    QString cmd(const QStringList &args, const QString &pwd);

  private slots:
    void slotSelfReadyReadStandardOutput();
    void slotSelfReadyReadStandardError();
    void slotActionOpenTriggered();

  private:
    QStringList m_args;
};

#endif /** __PYTHON_JOB_H__ */
