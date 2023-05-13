/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        home_view.cpp
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

#include "choose_mcu_dialog.h"

#include "home_view.h"
#include "ui_home_view.h"

home_view::home_view(QWidget *parent) : QWidget(parent), ui(new Ui::home_view)
{
    ui->setupUi(this);
}

home_view::~home_view()
{
    delete ui;
}

void home_view::on_button_create_mcu_project_clicked(bool checked)
{
    Q_UNUSED(checked)
    choose_mcu_dialog dialog(this);
    dialog.exec();
}

void home_view::on_button_create_board_project_clicked(bool checked)
{
    Q_UNUSED(checked)
}
