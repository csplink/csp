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
    (void)connect(ui->commandLinkButtonCreateChipProject, &QPushButton::clicked, this,
                  &ViewHome::pushButtonCreateChipProjectClickedCallback, Qt::UniqueConnection);
    (void)connect(ui->commandLinkButtonCreateBoardProject, &QPushButton::clicked, this,
                  &ViewHome::pushButtonCreateBoardProjectClickedCallback, Qt::UniqueConnection);
    (void)connect(ui->commandLinkButtonOpenExistingProject, &QPushButton::clicked, this,
                  &ViewHome::pushButtonOpenExistingProjectClickedCallback, Qt::UniqueConnection);
}

ViewHome::~ViewHome()
{
    delete ui;
}

void ViewHome::pushButtonCreateChipProjectClickedCallback(const bool checked)
{
    Q_UNUSED(checked)
    DialogChooseChip dialog(this);
    (void)connect(&dialog, &DialogChooseChip::finished, this, &ViewHome::dialogChooseChipFinishedCallback,
                  Qt::UniqueConnection);
    (void)connect(&dialog, &DialogChooseChip::signalCreateProject, this, &ViewHome::createChipProject,
                  Qt::UniqueConnection);
    (void)dialog.exec();
}

void ViewHome::pushButtonCreateBoardProjectClickedCallback(const bool checked) const
{
    Q_UNUSED(checked)
}

void ViewHome::dialogChooseChipFinishedCallback(const int result) const
{
    Q_UNUSED(result)
}

void ViewHome::pushButtonOpenExistingProjectClickedCallback(const bool checked)
{
    Q_UNUSED(checked)
    emit signalOpenExistingProject();
}

void ViewHome::createChipProject()
{
    Project.clearProject();
    Project.saveProject();
    emit signalCreateProject();
}
