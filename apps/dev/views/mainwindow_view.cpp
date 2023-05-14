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

#include "mainwindow_view.h"
#include "ui_mainwindow_view.h"

mainwindow_view::mainwindow_view(QWidget *parent) : QMainWindow(parent), ui(new Ui::mainwindow_view)
{
    ui->setupUi(this);
    ui->dockwidget_left->hide();
    ui->dockwidget_right->hide();
    ui->stackedwidget->setCurrentIndex(ENUM_STACK_INDEX_HOME);
}

mainwindow_view::~mainwindow_view()
{
    delete ui;
}

void mainwindow_view::on_action_new_triggered(bool checked)
{
    Q_UNUSED(checked)
}

void mainwindow_view::on_action_load_triggered(bool checked)
{
    Q_UNUSED(checked)
}

void mainwindow_view::on_action_save_triggered(bool checked)
{
    Q_UNUSED(checked)
}

void mainwindow_view::on_action_saveas_triggered(bool checked)
{
    Q_UNUSED(checked)
}

void mainwindow_view::on_action_close_triggered(bool checked)
{
    Q_UNUSED(checked)
}

void mainwindow_view::on_action_report_triggered(bool checked)
{
    Q_UNUSED(checked)
}
