/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        CspCoderJob.h
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

#ifndef __CSP_CODER_JOB_H__
#define __CSP_CODER_JOB_H__

#include "PythonJob.h"

class CspCoderJob final : public PythonJob
{
    Q_OBJECT
  public:
    explicit CspCoderJob(const QString &name);
    void generate(const QString &file);

  private:
    QString m_scriptFile;
    void start() override;
};

#endif /** __CSP_CODER_JOB_H__ */
