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

#include <QDir>
#include <QFile>
#include <QFileInfo>

#include "CspCoderJob.h"
#include "Settings.h"

CspCoderJob::CspCoderJob(const QString &name)
    : PythonJob(name, {}, true)
{
    m_scriptFile = QString("%1/csp-coder/csp-coder.py").arg(Settings.tools());
}

void CspCoderJob::generate(const QString &file)
{
    if (QFile::exists(file))
    {
        const QFileInfo info(file);
        const QStringList args = {
            m_scriptFile,
            QString("--file=%1").arg(file),
            QString("--output=%1").arg(info.dir().absolutePath()),
            QString("--repository=%1").arg(Settings.repository()),
        };
        setReadChannel(QProcess::StandardOutput);
        AbstractJob::start(Settings.python(), args);
    }
    else
    {
        /** TODO: error */
    }
}

void CspCoderJob::start()
{
}
