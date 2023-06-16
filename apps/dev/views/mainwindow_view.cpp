/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        mainwindow_view.cpp
 *  @brief
 *
 * ****************************************************************************
 *  @attention
 *  Licensed under the GNU General Public License v. 3 (the "License");
 *  You may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      https://www.gnu.org/licenses/gpl-3.0.html
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 *  Copyright (C) 2023-2023 xqyjlj<xqyjlj@126.com>
 *
 * ****************************************************************************
 *  Change Logs:
 *  Date           Author       Notes
 *  ------------   ----------   -----------------------------------------------
 *  2023-05-11     xqyjlj       initial version
 */

#include <QDebug>
#include <QStandardItem>

#include "chip_summary_table.h"
#include "mainwindow_view.h"
#include "ui_mainwindow_view.h"

mainwindow_view::mainwindow_view(QWidget *parent) : QMainWindow(parent), ui(new Ui::mainwindow_view)
{
    ui->setupUi(this);
    ui->dockwidget_left->hide();
    ui->dockwidget_right->hide();

    connect(ui->action_new_chip, &QAction::triggered, this, &mainwindow_view::action_new_chip_triggered_callback,
            Qt::UniqueConnection);
    connect(ui->action_load, &QAction::triggered, this, &mainwindow_view::action_load_triggered_callback,
            Qt::UniqueConnection);
    connect(ui->action_save, &QAction::triggered, this, &mainwindow_view::action_save_triggered_callback,
            Qt::UniqueConnection);
    connect(ui->action_saveas, &QAction::triggered, this, &mainwindow_view::action_saveas_triggered_callback,
            Qt::UniqueConnection);
    connect(ui->action_close, &QAction::triggered, this, &mainwindow_view::action_close_triggered_callback,
            Qt::UniqueConnection);
    connect(ui->action_report, &QAction::triggered, this, &mainwindow_view::action_report_triggered_callback,
            Qt::UniqueConnection);

    connect(ui->page_chip_configure_view, &chip_configure_view::signal_update_modules_treeview, this,
            &mainwindow_view::update_modules_treeview, Qt::UniqueConnection);
    ui->stackedwidget->setCurrentIndex(ENUM_STACK_INDEX_HOME);
}

mainwindow_view::~mainwindow_view()
{
    delete ui;
}

void mainwindow_view::update_modules_treeview(const QString &company, const QString &name)
{
    delete ui->treeview->model();

    ui->treeview->header()->hide();
    auto *model        = new QStandardItemModel(ui->treeview);
    auto  chip_summary = csp::chip_summary_table::load_chip_summary(company, name);
    auto  modules      = &chip_summary.modules;
    auto  modules_i    = modules->constBegin();
    while (modules_i != modules->constEnd())
    {
        auto item = new QStandardItem(modules_i.key());
        item->setEditable(false);
        model->appendRow(item);

        auto module   = &modules_i.value();
        auto module_i = module->constBegin();
        while (module_i != module->constEnd())
        {
            auto item_child = new QStandardItem(module_i.key());
            item_child->setEditable(false);
            item->appendRow(item_child);
            module_i++;
        }
        modules_i++;
    }
    ui->treeview->setModel(model);
    ui->treeview->expandAll();
}

void mainwindow_view::action_new_chip_triggered_callback(bool checked)
{
    Q_UNUSED(checked)
}

void mainwindow_view::action_load_triggered_callback(bool checked)
{
    Q_UNUSED(checked)
}

void mainwindow_view::action_save_triggered_callback(bool checked)
{
    Q_UNUSED(checked)
}

void mainwindow_view::action_saveas_triggered_callback(bool checked)
{
    Q_UNUSED(checked)
}

void mainwindow_view::action_close_triggered_callback(bool checked)
{
    Q_UNUSED(checked)
}

void mainwindow_view::action_report_triggered_callback(bool checked)
{
    Q_UNUSED(checked)
}
