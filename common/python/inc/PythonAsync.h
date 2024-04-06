/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        PythonAsync.h
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
 * 2024-04-06     xqyjlj       initial version
 */

#ifndef CSP_PYTHON_ASYNC_H
#define CSP_PYTHON_ASYNC_H

#include <QObject>
#include <QProcess>
#include <QString>

#include "Config.h"

class PythonAsync final : public QObject
{
    Q_OBJECT

  public:
    static void init();
    static void deinit();

    int execv(const QStringList &argv, const QString &workDir = Config::defaultWorkDir());
    static PythonAsync *getInstance();

  signals:
    void signalReadyReadStandardOutput(const QProcess *process, const QString &msg);
    void signalFinished(const QProcess *process, int exitCode, QProcess::ExitStatus exitStatus);

  private:
    inline static PythonAsync *instance_ = nullptr;
    PythonAsync() = default;
    ~PythonAsync() override = default;

    Q_DISABLE_COPY_MOVE(PythonAsync)
};

#endif /** CSP_XMAKE_ASYNC_H */
