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
    (void)connect(ui_->comboBoxPackageVersion, &QComboBox::currentTextChanged, this, &ViewConfigure::comboBoxPackageVersionCurrentTextChanged, Qt::UniqueConnection);
    (void)connect(ui_->comboBoxBuildScriptIde, &QComboBox::currentTextChanged, this, &ViewConfigure::comboBoxBuildScriptIdeCurrentTextChanged, Qt::UniqueConnection);
    (void)connect(ui_->comboBoxBuildScriptIdeMinVersion, &QComboBox::currentTextChanged, this, &ViewConfigure::comboBoxBuildScriptIdeMinVersionCurrentTextChanged, Qt::UniqueConnection);
    (void)connect(ui_->checkBoxEnableToolchains, &QCheckBox::stateChanged, this, &ViewConfigure::checkBoxEnableToolchainsStateChanged, Qt::UniqueConnection);
    (void)connect(ui_->comboBoxToolchainsVersion, &QComboBox::currentTextChanged, this, &ViewConfigure::comboBoxToolchainsVersionCurrentTextChanged, Qt::UniqueConnection);

    initProjectSettings();
    initLinkerSettings();
    initPackageSettings();
    initToolchainsSettings();
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
         * 0: View initialization
         * 1: Layout initialization
         * 2: Global maximization
         */
        resizeCounter_++;
    }
    QWidget::resizeEvent(event);
}

void ViewConfigure::initProjectSettings() const
{
    const ChipSummaryTable::TargetProjectType &target_project = projectInstance_->getChipSummary().TargetProject;

    ui_->comboBoxBuildScriptIde->clear();

    const QString target = projectInstance_->getProjectTargetProject();

    if (target_project.XMake)
    {
        ui_->comboBoxBuildScriptIde->addItem("XMake");
        if (target == "XMake")
        {
            ui_->comboBoxBuildScriptIde->setCurrentText(target);
        }
    }
    if (target_project.CMake)
    {
        ui_->comboBoxBuildScriptIde->addItem("CMake");
        if (target == "CMake")
        {
            ui_->comboBoxBuildScriptIde->setCurrentText(target);
        }
    }
    if (!target_project.MdkArm.Versions.isEmpty())
    {
        ui_->comboBoxBuildScriptIde->addItem("MDK-Arm");
        if (target == "MDK-Arm")
        {
            ui_->comboBoxBuildScriptIde->setCurrentText(target);
        }
    }
}

void ViewConfigure::flushComboBoxPackageVersion() const
{
    const QString &hal = projectInstance_->getProjectHal();
    ToolCspRepo::PackageType packages;
    ToolCspRepo::loadPackages(&packages, hal);

    const QString text = projectInstance_->getProjectHalVersion();
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

void ViewConfigure::flushComboBoxToolchainsVersionVersion() const
{
    const QString &toolchainsVersion = ui_->lineEditToolchainsName->text();
    ToolCspRepo::PackageType packages;
    ToolCspRepo::loadPackages(&packages, toolchainsVersion);

    const QString text = projectInstance_->getProjectToolchainsVersion();
    auto &versions = packages["Toolchains"][toolchainsVersion].Versions;

    if (versions.keys().contains(text))
    {
        ui_->checkBoxEnableToolchains->setCheckState(Qt::Checked);
    }
    else
    {
        ui_->checkBoxEnableToolchains->setCheckState(Qt::Unchecked);
    }

    ui_->comboBoxToolchainsVersion->clear();
    auto versionsI = versions.constBegin();
    while (versionsI != versions.constEnd())
    {
        if (versionsI.value().Installed)
        {
            ui_->comboBoxToolchainsVersion->addItem(versionsI.key());
            if (versionsI.key() == text)
            {
                ui_->comboBoxToolchainsVersion->setCurrentText(text);
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

    flushComboBoxPackageVersion();
}

void ViewConfigure::initToolchainsSettings() const
{
    const ChipSummaryTable::ChipSummaryType &chip_summary = projectInstance_->getChipSummary();

    if (!chip_summary.Toolchains.isEmpty())
    {
        ui_->lineEditToolchainsName->setText(chip_summary.Toolchains);
    }

    flushComboBoxToolchainsVersionVersion();
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

void ViewConfigure::comboBoxPackageVersionCurrentTextChanged(const QString &text)
{
    projectInstance_->setProjectHalVersion(text);
}

void ViewConfigure::comboBoxBuildScriptIdeCurrentTextChanged(const QString &text)
{
    projectInstance_->setProjectTargetProject(text);
    if (text == "XMake")
    {
        ui_->widgetBoxBuildScriptIdeMinVersion->setVisible(false);
    }
    else if (text == "CMake")
    {
        ui_->widgetBoxBuildScriptIdeMinVersion->setVisible(false);
    }
    else if (text == "MDK-Arm")
    {
        const ChipSummaryTable::TargetProjectType &target_project = projectInstance_->getChipSummary().TargetProject;
        const QString minVersion = projectInstance_->getProjectTargetProjectMinVersion();
        ui_->comboBoxBuildScriptIdeMinVersion->clear();
        for (const QString &version : qAsConst(target_project.MdkArm.Versions))
        {
            ui_->comboBoxBuildScriptIdeMinVersion->addItem(version);
            if (version == minVersion)
            {
                ui_->comboBoxBuildScriptIdeMinVersion->setCurrentText(version);
            }
        }
        ui_->widgetBoxBuildScriptIdeMinVersion->setVisible(true);
    }
}

void ViewConfigure::comboBoxBuildScriptIdeMinVersionCurrentTextChanged(const QString &text)
{
    projectInstance_->setProjectTargetProjectMinVersion(text);
}

void ViewConfigure::checkBoxEnableToolchainsStateChanged(int State)
{
    if (Qt::Unchecked == State)
    {
        ui_->comboBoxToolchainsVersion->setEnabled(false);
        ui_->pushButtonToolchainsManager->setEnabled(false);
        projectInstance_->setProjectToolchainsVersion("");
    }
    else
    {
        ui_->comboBoxToolchainsVersion->setEnabled(true);
        ui_->pushButtonToolchainsManager->setEnabled(true);
    }
}

void ViewConfigure::pushButtonToolchainsManagerPressedCallback()
{
    DialogPackageManager dialog(this);
    (void)dialog.exec();
    flushComboBoxToolchainsVersionVersion();
}

void ViewConfigure::comboBoxToolchainsVersionCurrentTextChanged(const QString &text)
{
    if (ui_->checkBoxEnableToolchains->checkState() == Qt::Checked)
    {
        projectInstance_->setProjectToolchainsVersion(text);
    }
}
