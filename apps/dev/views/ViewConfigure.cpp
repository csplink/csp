/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ViewConfigure.cpp
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
 *  2023-05-14     xqyjlj       initial version
 */

#include <QtCore>

#include "DialogPackageManager.h"
#include "GraphicsItemPin.h"
#include "LQFP.h"
#include "ToolCspRepo.h"
#include "ViewConfigure.h"
#include "ui_ViewConfigure.h"

ViewConfigure::ViewConfigure(QWidget *parent)
    : QWidget(parent), ui_(new Ui::viewConfigure)
{
    ui_->setupUi(this);
    projectInstance_ = Project::getInstance();

    (void)connect(ui_->pushButtonPackageManager, &QPushButton::pressed, this, &ViewConfigure::pushButtonPackageManagerPressedCallback, Qt::UniqueConnection);
    (void)connect(ui_->pushButtonZoomIn, &QPushButton::pressed, this, &ViewConfigure::pushButtonZoomInPressedCallback, Qt::UniqueConnection);
    (void)connect(ui_->pushButtonZoomReset, &QPushButton::pressed, this, &ViewConfigure::pushButtonZoomResetPressedCallback, Qt::UniqueConnection);
    (void)connect(ui_->pushButtonZoomOut, &QPushButton::pressed, this, &ViewConfigure::pushButtonZoomOutPressedCallback, Qt::UniqueConnection);

    initProjectSettings();
    initLinkerSettings();
    initPackageSettings();
}

ViewConfigure::~ViewConfigure()
{
    delete ui_;
}

void ViewConfigure::showEvent(QShowEvent *event)
{
    Q_UNUSED(event);
}

void ViewConfigure::setPropertyBrowser(PropertyBrowserPin *instance)
{
    propertyBrowserInstance_ = instance;

    (void)connect(ui_->graphicsView, &GraphicsViewPanZoom::signalsSelectedItemClicked, propertyBrowserInstance_, &PropertyBrowserPin::updatePropertyByPin);
}

void ViewConfigure::initView()
{
    const auto package = projectInstance_->getProjectPackage().toLower();
    const auto hal = projectInstance_->getProjectHal().toLower();
    const auto company = projectInstance_->getProjectCompany();
    const auto name = projectInstance_->getProjectTargetChip();

    delete ui_->graphicsView->scene();
    const auto scene = new QGraphicsScene(ui_->graphicsView);
    if (package.startsWith("lqfp"))
    {
        LQFP lqfp(nullptr);
        auto items = lqfp.getLqfp(hal, company, name);
        for (const auto &item : items)
        {
            scene->addItem(item);
            if ((item->flags() & QGraphicsItem::ItemIsFocusable) == QGraphicsItem::ItemIsFocusable)
            {
                (void)connect(dynamic_cast<const GraphicsItemPin *>(item), &GraphicsItemPin::signalPropertyChanged, ui_->graphicsView,
                              &GraphicsViewPanZoom::propertyChangedCallback, Qt::UniqueConnection);
            }
        }
    }
    ui_->graphicsView->setScene(scene);
}

void ViewConfigure::resizeEvent(QResizeEvent *event)
{
    if (resizeCounter_ <= 2)
    {
        ui_->graphicsView->resize();

        /**
         * 0: 视图初始化
         * 1: 布局初始化
         * 2: 全局最大化
         */
        resizeCounter_++;
    }
    QWidget::resizeEvent(event);
}

void ViewConfigure::initProjectSettings() const
{
    const ChipSummaryTable::TargetProjectType &target_project = projectInstance_->getChipSummary().TargetProject;

    ui_->comboBoxBuildScriptIde->clear();

    if (target_project.XMake)
    {
        ui_->comboBoxBuildScriptIde->addItem("XMake");
    }
    if (target_project.CMake)
    {
        ui_->comboBoxBuildScriptIde->addItem("CMake");
    }
    if (!target_project.MdkArm.Device.isEmpty())
    {
        ui_->comboBoxBuildScriptIde->addItem("MDK-Arm");
    }

    flushComboBoxPackageVersion();
}

void ViewConfigure::flushComboBoxPackageVersion() const
{
    const QString &hal = projectInstance_->getProjectHal();
    ToolCspRepo::PackageType packages;
    ToolCspRepo::loadPackages(&packages, hal);

    const QString text = ui_->comboBoxPackageVersion->currentText();
    ui_->comboBoxPackageVersion->clear();

    auto &versions = packages["Library"][hal].Versions;
    auto versionsI = versions.constBegin();
    while (versionsI != versions.constEnd())
    {
        if (versionsI.value().Installed)
        {
            ui_->comboBoxPackageVersion->addItem(versionsI.key());
            if (versionsI.key() == text)
            {
                ui_->comboBoxPackageVersion->setCurrentText(text);
            }
        }
        ++versionsI;
    }
}

void ViewConfigure::initLinkerSettings() const
{
    const ChipSummaryTable::LinkerType &linker = projectInstance_->getChipSummary().Linker;
    ui_->lineEditMinimumHeapSize->clear();
    if (!linker.DefaultMinimumHeapSize.isEmpty())
    {
        ui_->lineEditMinimumHeapSize->setText(linker.DefaultMinimumHeapSize);
    }
    else
    {
        ui_->lineEditMinimumHeapSize->setReadOnly(true);
        ui_->lineEditMinimumHeapSize->setDisabled(true);
    }

    ui_->lineEditMinimumStackSize->clear();
    if (!linker.DefaultMinimumStackSize.isEmpty())
    {
        ui_->lineEditMinimumStackSize->setText(linker.DefaultMinimumStackSize);
    }
    else
    {
        ui_->lineEditMinimumStackSize->setReadOnly(true);
        ui_->lineEditMinimumStackSize->setDisabled(true);
    }
}

void ViewConfigure::initPackageSettings() const
{
    const ChipSummaryTable::ChipSummaryType &chip_summary = projectInstance_->getChipSummary();

    if (!chip_summary.Hal.isEmpty())
    {
        ui_->lineEditPackageName->setText(chip_summary.Hal);
    }
}

void ViewConfigure::pushButtonPackageManagerPressedCallback()
{
    DialogPackageManager dialog(this);
    (void)dialog.exec();
    flushComboBoxPackageVersion();
}

void ViewConfigure::pushButtonZoomInPressedCallback() const
{
    ui_->graphicsView->zoomIn(6);
}

void ViewConfigure::pushButtonZoomResetPressedCallback() const
{
    ui_->graphicsView->resize();
}

void ViewConfigure::pushButtonZoomOutPressedCallback() const
{
    ui_->graphicsView->zoomOut(6);
}
