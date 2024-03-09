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

#include "dialog_choose_chip.h"

#include "home_view.h"
#include "ui_home_view.h"

home_view::home_view(QWidget *parent)
    : QWidget(parent), _ui(new Ui::home_view)
{
    _ui->setupUi(this);
    (void)connect(_ui->button_create_mcu_project, &QPushButton::clicked, this,
                  &home_view::button_create_chip_project_clicked_callback, Qt::UniqueConnection);
    (void)connect(_ui->button_create_board_project, &QPushButton::clicked, this,
                  &home_view::button_create_board_project_clicked_callback, Qt::UniqueConnection);
    (void)connect(_ui->button_open_existing_project, &QPushButton::clicked, this,
                  &home_view::button_open_existing_project_clicked_callback, Qt::UniqueConnection);

    _project_instance = project::get_instance();
}

home_view::~home_view()
{
    delete _ui;
}

void home_view::button_create_chip_project_clicked_callback(const bool checked)
{
    Q_UNUSED(checked)
    dialog_choose_chip dialog(this);
    (void)connect(&dialog, &dialog_choose_chip::finished, this, &home_view::dialog_choose_chip_finished_callback,
                  Qt::UniqueConnection);
    (void)connect(&dialog, &dialog_choose_chip::signals_create_project, this, &home_view::create_chip_project,
                  Qt::UniqueConnection);
    (void)dialog.exec();
}

void home_view::button_create_board_project_clicked_callback(const bool checked)
{
    Q_UNUSED(checked)
}

void home_view::dialog_choose_chip_finished_callback(const int result)
{
    Q_UNUSED(result)
}

void home_view::button_open_existing_project_clicked_callback(const bool checked)
{
    Q_UNUSED(checked)
    emit signal_open_existing_project(true);
}

void home_view::create_chip_project()
{
    _project_instance->clear_project();
    _project_instance->save_project();
    emit signal_create_project();
}
