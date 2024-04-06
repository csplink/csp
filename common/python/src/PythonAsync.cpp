/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        PythonAsync.cpp
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

#include <QDir>
#include <QMutex>
#include <QProcess>

#include "PythonAsync.h"

void PythonAsync::init()
{
    if (instance_ == nullptr)
    {
        instance_ = new PythonAsync();
    }
}

void PythonAsync::deinit()
{
    delete instance_;
    instance_ = nullptr;
}

PythonAsync *PythonAsync::getInstance()
{
    return instance_;
}

int PythonAsync::execv(const QStringList &argv, const QString &workDir)
{
    static QMutex mutex;
    QMutexLocker locker(&mutex);

    const QString program = Config::toolPython();
    const QMap<QString, QString> env = Config::env();

    QProcessEnvironment environment = QProcessEnvironment::systemEnvironment();
    auto envIterator = env.constBegin();
    while (envIterator != env.constEnd())
    {
        environment.insert(envIterator.key(), envIterator.value());
        ++envIterator;
    }
    QProcess *process = new QProcess();
    process->setProgram(program);
    process->setArguments(argv);
    process->setProcessEnvironment(environment);

    const QDir dir(workDir);
    if (dir.exists())
    {
        process->setWorkingDirectory(workDir);
    }

    connect(process, &QProcess::readyReadStandardOutput, this,
            [process, this]() {
                const QByteArray output = process->readAllStandardOutput();
                emit signalReadyReadStandardOutput(process, output);
            });
    connect(process, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished), process,
            [process, this](const int exitCode, const QProcess::ExitStatus exitStatus) {
                emit signalFinished(process, exitCode, exitStatus);
                process->deleteLater();
            });

    process->start();
    process->waitForFinished(30000);
    return process->exitCode();
}
