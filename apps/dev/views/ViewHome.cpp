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

#include "ViewHome.h"
#include "ui_ViewHome.h"

ViewHome::ViewHome(QWidget *parent)
    : QWidget(parent), ui_(new Ui::viewHome)
{
    ui_->setupUi(this);
    (void)connect(ui_->commandLinkButtonCreateChipProject, &QPushButton::clicked, this, &ViewHome::pushButtonCreateChipProjectClickedCallback, Qt::UniqueConnection);
    (void)connect(ui_->commandLinkButtonCreateBoardProject, &QPushButton::clicked, this, &ViewHome::pushButtonCreateBoardProjectClickedCallback, Qt::UniqueConnection);
    (void)connect(ui_->commandLinkButtonOpenExistingProject, &QPushButton::clicked, this, &ViewHome::pushButtonOpenExistingProjectClickedCallback, Qt::UniqueConnection);

    projectInstance_ = Project::getInstance();
}

ViewHome::~ViewHome()
{
    delete ui_;
}

void ViewHome::pushButtonCreateChipProjectClickedCallback(const bool checked)
{
    Q_UNUSED(checked)
    DialogChooseChip dialog(this);
    (void)connect(&dialog, &DialogChooseChip::finished, this, &ViewHome::dialogChooseChipFinishedCallback,
                  Qt::UniqueConnection);
    (void)connect(&dialog, &DialogChooseChip::signalsCreateProject, this, &ViewHome::createChipProject,
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
    emit signalOpenExistingProject(true);
}

void ViewHome::createChipProject()
{
    projectInstance_->clearProject();
    projectInstance_->saveProject();
    emit signalCreateProject();
}
