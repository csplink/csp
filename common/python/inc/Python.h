/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        Python.h
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
#ifndef CSP_PYTHON_H
#define CSP_PYTHON_H

#include <QDebug>
#include <QObject>
#include <QString>

#include "PythonAsync.h"

class Python final : public QObject
{
    Q_OBJECT

  public:
    static void init();
    static void deinit();
    static QString version();
    static bool execv(const QStringList &argv, QByteArray *output, QByteArray *error);
    static QString cmd(const QString &command, const QStringList &args = {});

  private:
    Python();
    ~Python() override;

    Q_DISABLE_COPY_MOVE(Python)
};

#endif /** CSP_PYTHON_H */
