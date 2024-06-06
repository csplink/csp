/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        DockModuleTree.h
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
 * 2024-05-01     xqyjlj       initial version
 */

#ifndef DOCK_MODULE_TREE_H
#define DOCK_MODULE_TREE_H

#include <QDockWidget>

#include "ChipSummaryTable.h"

namespace Ui
{
class DockModuleTree;
}

class DockModuleTree : public QDockWidget
{
    Q_OBJECT

  public:
    explicit DockModuleTree(QWidget *parent = nullptr);
    ~DockModuleTree() override;

    void setModule(const ChipSummaryTable::ChipSummaryType &chipSummary) const;

  public slots:
    void setModule(const QString &vendor, const QString &name) const;

  private:
    Ui::DockModuleTree *ui;
};

#endif /** DOCK_MODULE_TREE_H */
