/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        DockModuleTree.cpp
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
#include <QStandardItemModel>

#include "DockModuleTree.h"
#include "ui_DockModuleTree.h"

DockModuleTree::DockModuleTree(QWidget *parent)
    : QDockWidget(parent),
      ui(new Ui::DockModuleTree)
{
    ui->setupUi(this);
}

DockModuleTree::~DockModuleTree()
{
    delete ui;
}

void DockModuleTree::setModule(const ChipSummaryTable::ChipSummaryType &chipSummary) const
{
    ui->treeViewModule->header()->hide();
    auto *model = new QStandardItemModel(ui->treeViewModule);

    const ChipSummaryTable::ModulesType modules = chipSummary.Modules;
    auto modules_i = modules.constBegin();
    while (modules_i != modules.constEnd())
    {
        const auto item = new QStandardItem(modules_i.key());
        item->setEditable(false);
        model->appendRow(item);

        const auto module = &modules_i.value();
        auto module_i = module->constBegin();
        while (module_i != module->constEnd())
        {
            const auto item_child = new QStandardItem(module_i.key());
            item_child->setEditable(false);
            item->appendRow(item_child);
            ++module_i;
        }
        ++modules_i;
    }
    delete ui->treeViewModule->model();
    ui->treeViewModule->setModel(model);
    ui->treeViewModule->expandAll();
}

void DockModuleTree::setModule(const QString &company, const QString &name) const
{
    ChipSummaryTable::ChipSummaryType chipSummary;
    ChipSummaryTable::loadChipSummary(&chipSummary, company, name);

    setModule(chipSummary);
}
