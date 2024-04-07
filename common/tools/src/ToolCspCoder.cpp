/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        ToolCspCoder.cpp
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
 * 2024-04-05     xqyjlj       initial version
 */
#include <QDir>
#include <QFile>
#include <QFileInfo>

#include "Config.h"
#include "PythonAsync.h"
#include "ToolCspCoder.h"

ToolCspCoder::ToolCspCoder() = default;

ToolCspCoder::~ToolCspCoder() = default;

int ToolCspCoder::generate(const QString &file)
{
    int err = -1;
    if (QFile::exists(file))
    {
        const QFileInfo info(file);
        PythonAsync *python = PythonAsync::getInstance();
        const QString scriptFile = QString("%1/csp-coder/csp-coder.py").arg(Config::toolsDir());
        err = python->execv({ scriptFile, QString("--file=%1").arg(file),
                              QString("--output=%1").arg(info.dir().absolutePath()),
                              QString("--repositories=%1").arg(Config::repositoriesDir()) });
    }
    else
    {
        /** TODO: error */
    }
    return err;
}
