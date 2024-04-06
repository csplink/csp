/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        ToolCspCoder.h
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

#ifndef CSP_TOOL_CSP_CODER_H
#define CSP_TOOL_CSP_CODER_H

#include "Python.h"

class ToolCspCoder final : public QObject
{
    Q_OBJECT

  public:
  private:
    ToolCspCoder();
    ~ToolCspCoder() override;

    Q_DISABLE_COPY_MOVE(ToolCspCoder)
};

#endif /** CSP_TOOL_CSP_REPO_H */
