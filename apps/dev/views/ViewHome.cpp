/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ViewHome.cpp
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

#include "DialogChooseChip.h"
#include "Project.h"
#include "ViewHome.h"
#include "ui_ViewHome.h"

ViewHome::ViewHome(QWidget *parent)
    : QWidget(parent),
      ui(new Ui::viewHome)
{
    ui->setupUi(this);
    (void)connect(ui->commandLinkButtonCreateChipProject, &QPushButton::pressed, this,
                  &ViewHome::slotPushButtonCreateChipProjectPressed);
    (void)connect(ui->commandLinkButtonCreateBoardProject, &QPushButton::pressed, this,
                  &ViewHome::slotPushButtonCreateBoardProjectPressed);
    (void)connect(ui->commandLinkButtonOpenExistingProject, &QPushButton::pressed, this,
                  &ViewHome::slotPushButtonOpenExistingProjectPressed);
}

ViewHome::~ViewHome()
{
    delete ui;
}

void ViewHome::slotPushButtonCreateChipProjectPressed()
{
    DialogChooseChip dialog(this);
    (void)dialog.exec();
}

void ViewHome::slotPushButtonCreateBoardProjectPressed() const
{
}

void ViewHome::slotPushButtonOpenExistingProjectPressed()
{
    Project.loadProjectWithDialog(this);
}
