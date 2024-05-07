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

#include "CspRepoJob.h"
#include "DialogPackageManager.h"
#include "GraphicsItemPin.h"
#include "LQFP.h"
#include "Repo.h"
#include "ViewConfigure.h"
#include "ui_ViewConfigure.h"

ViewConfigure::ViewConfigure(QWidget *parent)
    : QWidget(parent),
      ui(new Ui::viewConfigure),
      m_propertyBrowserInstance(nullptr),
      m_resizeCounter(0)
{
    ui->setupUi(this);

    ui->lineEditHeapSize->setValidator(new QRegExpValidator(QRegExp(R"(^0x[0-9A-Fa-f]+$)")));
    ui->lineEditStackSize->setValidator(new QRegExpValidator(QRegExp(R"(^0x[0-9A-Fa-f]+$)")));

    {
        (void)connect(ui->pushButtonPackageManager, &QPushButton::pressed, this,
                      &ViewConfigure::slotPushButtonPackageManagerPressed, Qt::UniqueConnection);
        (void)connect(ui->pushButtonZoomIn, &QPushButton::pressed, this, &ViewConfigure::slotPushButtonZoomInPressed,
                      Qt::UniqueConnection);
        (void)connect(ui->pushButtonZoomReset, &QPushButton::pressed, this,
                      &ViewConfigure::slotPushButtonZoomResetPressed, Qt::UniqueConnection);
        (void)connect(ui->pushButtonZoomOut, &QPushButton::pressed, this, &ViewConfigure::slotPushButtonZoomOutPressed,
                      Qt::UniqueConnection);
        (void)connect(ui->comboBoxPackageVersion, &QComboBox::currentTextChanged, this,
                      &ViewConfigure::slotComboBoxPackageVersionCurrentTextChanged, Qt::UniqueConnection);
        (void)connect(ui->comboBoxBuildScriptIde, &QComboBox::currentTextChanged, this,
                      &ViewConfigure::slotComboBoxBuildScriptIdeCurrentTextChanged, Qt::UniqueConnection);
        (void)connect(ui->comboBoxBuildScriptIdeMinVersion, &QComboBox::currentTextChanged, this,
                      &ViewConfigure::slotComboBoxBuildScriptIdeMinVersionCurrentTextChanged, Qt::UniqueConnection);
        (void)connect(ui->checkBoxEnableToolchains, &QCheckBox::stateChanged, this,
                      &ViewConfigure::slotCheckBoxEnableToolchainsStateChanged, Qt::UniqueConnection);
        (void)connect(ui->comboBoxToolchainsVersion, &QComboBox::currentTextChanged, this,
                      &ViewConfigure::slotComboBoxToolchainsVersionCurrentTextChanged, Qt::UniqueConnection);
    }

    (void)connect(&Project, &CspProject::signalReloaded, this, &ViewConfigure::slotProjectReloaded);

    initView();
}

ViewConfigure::~ViewConfigure()
{
    delete ui;
}

void ViewConfigure::resizeEvent(QResizeEvent *event)
{
    if (m_resizeCounter <= 2)
    {
        ui->graphicsView->resize();

        /**
         * 0: View initialization
         * 1: Layout initialization
         * 2: Global maximization
         */
        m_resizeCounter++;
    }
    QWidget::resizeEvent(event);
}

void ViewConfigure::setPropertyBrowser(PropertyBrowserPin *instance)
{
    m_propertyBrowserInstance = instance;

    (void)connect(ui->graphicsView, &GraphicsViewPanZoom::signalsSelectedItemClicked, m_propertyBrowserInstance,
                  &PropertyBrowserPin::updatePropertyByPin);
}

void ViewConfigure::initView()
{
    initMainView();
    initProjectSettings();
    initLinkerSettings();
    initPackageSettings();
    initToolchainsSettings();
}

void ViewConfigure::initMainView()
{
    const QString package = Project.package().toLower();
    const QString hal = Project.hal().toLower();
    const QString company = Project.company();
    const QString targetChip = Project.targetChip();

    delete ui->graphicsView->scene();
    const auto scene = new QGraphicsScene(ui->graphicsView);
    if (package.startsWith("lqfp"))
    {
        LQFP lqfp(nullptr);
        auto items = lqfp.getLqfp(hal, company, targetChip);
        for (const auto &item : items)
        {
            scene->addItem(item);
            if ((item->flags() & QGraphicsItem::ItemIsFocusable) == QGraphicsItem::ItemIsFocusable)
            {
                (void)connect(dynamic_cast<const GraphicsItemPin *>(item), &GraphicsItemPin::signalPropertyChanged,
                              ui->graphicsView, &GraphicsViewPanZoom::propertyChangedCallback, Qt::UniqueConnection);
            }
        }
    }
    ui->graphicsView->setScene(scene);
    ui->graphicsView->resize();
}

void ViewConfigure::initProjectSettings() const
{
    const ChipSummaryTable::TargetProjectType &targetProject =
        Repo.getChipSummary(Project.company(), Project.targetChip()).TargetProject;

    ui->comboBoxBuildScriptIde->clear();

    const QString target = Project.targetProject();

    if (targetProject.XMake)
    {
        ui->comboBoxBuildScriptIde->addItem("XMake");
        if (target == "XMake")
        {
            ui->comboBoxBuildScriptIde->setCurrentText(target);
        }
    }
    if (targetProject.CMake)
    {
        ui->comboBoxBuildScriptIde->addItem("CMake");
        if (target == "CMake")
        {
            ui->comboBoxBuildScriptIde->setCurrentText(target);
        }
    }
    if (!targetProject.MdkArm.Versions.isEmpty())
    {
        ui->comboBoxBuildScriptIde->addItem("MDK-Arm");
        if (target == "MDK-Arm")
        {
            ui->comboBoxBuildScriptIde->setCurrentText(target);
        }
    }
}

void ViewConfigure::flushComboBoxPackageVersion() const
{
    const QString hal = Project.hal();
    CspRepoJob::PackageType packages;
    CspRepoJob job("repo");
    job.loadPackages(&packages, hal);

    const QString text = Project.halVersion();
    ui->comboBoxPackageVersion->clear();

    auto &versions = packages["Library"][hal].Versions;
    auto versionsI = versions.constBegin();
    while (versionsI != versions.constEnd())
    {
        if (versionsI.value().Installed)
        {
            ui->comboBoxPackageVersion->addItem(versionsI.key());
            if (versionsI.key() == text)
            {
                ui->comboBoxPackageVersion->setCurrentText(text);
            }
        }
        ++versionsI;
    }
}

void ViewConfigure::flushComboBoxToolchainsVersionVersion() const
{
    const QString &toolchainsVersion = ui->lineEditToolchainsName->text();
    CspRepoJob::PackageType packages;
    CspRepoJob job("repo");
    job.loadPackages(&packages, toolchainsVersion);

    const QString text = Project.toolchainsVersion();
    auto &versions = packages["Toolchains"][toolchainsVersion].Versions;

    if (versions.keys().contains(text))
    {
        ui->checkBoxEnableToolchains->setCheckState(Qt::Checked);
    }
    else
    {
        ui->checkBoxEnableToolchains->setCheckState(Qt::Unchecked);
    }

    ui->comboBoxToolchainsVersion->clear();
    auto versionsI = versions.constBegin();
    while (versionsI != versions.constEnd())
    {
        if (versionsI.value().Installed)
        {
            ui->comboBoxToolchainsVersion->addItem(versionsI.key());
            if (versionsI.key() == text)
            {
                ui->comboBoxToolchainsVersion->setCurrentText(text);
            }
        }
        ++versionsI;
    }
}

void ViewConfigure::initLinkerSettings() const
{
    ui->lineEditHeapSize->clear();
    if (!Project.linkerHeapSize().isEmpty())
    {
        ui->lineEditHeapSize->setText(Project.linkerHeapSize());
        (void)connect(ui->lineEditHeapSize, &QLineEdit::textChanged, this,
                      &ViewConfigure::slotLineEditHeapSizeTextChanged);
    }
    else
    {
        (void)disconnect(ui->lineEditHeapSize, &QLineEdit::textChanged, this,
                         &ViewConfigure::slotLineEditHeapSizeTextChanged);
        ui->lineEditHeapSize->setReadOnly(true);
        ui->lineEditHeapSize->setDisabled(true);
    }

    ui->lineEditStackSize->clear();
    if (!Project.linkerStackSize().isEmpty())
    {
        ui->lineEditStackSize->setText(Project.linkerStackSize());
        (void)connect(ui->lineEditStackSize, &QLineEdit::textChanged, this,
                      &ViewConfigure::slotLineEditStackSizeTextChanged);
    }
    else
    {
        (void)disconnect(ui->lineEditStackSize, &QLineEdit::textChanged, this,
                         &ViewConfigure::slotLineEditStackSizeTextChanged);
        ui->lineEditStackSize->setReadOnly(true);
        ui->lineEditStackSize->setDisabled(true);
    }
}

void ViewConfigure::initPackageSettings() const
{
    const ChipSummaryTable::ChipSummaryType &chip_summary =
        Repo.getChipSummary(Project.company(), Project.targetChip());

    if (!chip_summary.Hal.isEmpty())
    {
        ui->lineEditPackageName->setText(chip_summary.Hal);
    }

    flushComboBoxPackageVersion();
}

void ViewConfigure::initToolchainsSettings() const
{
    const ChipSummaryTable::ChipSummaryType &chip_summary =
        Repo.getChipSummary(Project.company(), Project.targetChip());

    if (!chip_summary.Toolchains.isEmpty())
    {
        ui->lineEditToolchainsName->setText(chip_summary.Toolchains);
    }

    flushComboBoxToolchainsVersionVersion();
}

void ViewConfigure::slotPushButtonPackageManagerPressed()
{
    DialogPackageManager dialog(this);
    (void)dialog.exec();
    flushComboBoxPackageVersion();
}

void ViewConfigure::slotPushButtonZoomInPressed() const
{
    ui->graphicsView->zoomIn(6);
}

void ViewConfigure::slotPushButtonZoomResetPressed() const
{
    ui->graphicsView->resize();
}

void ViewConfigure::slotPushButtonZoomOutPressed() const
{
    ui->graphicsView->zoomOut(6);
}

void ViewConfigure::slotComboBoxPackageVersionCurrentTextChanged(const QString &text)
{
    Project.setHalVersion(text);
}

void ViewConfigure::slotComboBoxBuildScriptIdeCurrentTextChanged(const QString &text)
{
    if (!text.isEmpty())
    {
        Project.setTargetProject(text);

        if (text == "MDK-Arm")
        {
            const ChipSummaryTable::TargetProjectType &targetProject =
                Repo.getChipSummary(Project.company(), Project.targetChip()).TargetProject;
            const QString minVersion = Project.targetProjectMinVersion();
            ui->comboBoxBuildScriptIdeMinVersion->clear();
            for (const QString &version : qAsConst(targetProject.MdkArm.Versions))
            {
                ui->comboBoxBuildScriptIdeMinVersion->addItem(version);
                if (version == minVersion)
                {
                    ui->comboBoxBuildScriptIdeMinVersion->setCurrentText(version);
                }
            }
            ui->widgetBoxBuildScriptIdeMinVersion->setVisible(true);
        }
        else
        {
            ui->widgetBoxBuildScriptIdeMinVersion->setVisible(false);
        }
    }
}

void ViewConfigure::slotComboBoxBuildScriptIdeMinVersionCurrentTextChanged(const QString &text)
{
    Project.setTargetProjectMinVersion(text);
}

void ViewConfigure::slotCheckBoxEnableToolchainsStateChanged(int State)
{
    if (Qt::Unchecked == State)
    {
        ui->comboBoxToolchainsVersion->setEnabled(false);
        ui->pushButtonToolchainsManager->setEnabled(false);
        Project.setToolchainsVersion("");
    }
    else
    {
        ui->comboBoxToolchainsVersion->setEnabled(true);
        ui->pushButtonToolchainsManager->setEnabled(true);
    }
}

void ViewConfigure::slotPushButtonToolchainsManagerPressed()
{
    DialogPackageManager dialog(this);
    (void)dialog.exec();
    flushComboBoxToolchainsVersionVersion();
}

void ViewConfigure::slotComboBoxToolchainsVersionCurrentTextChanged(const QString &text)
{
    if (ui->checkBoxEnableToolchains->checkState() == Qt::Checked)
    {
        Project.setToolchainsVersion(text);
    }
}

void ViewConfigure::slotProjectReloaded()
{
    initView();
}

void ViewConfigure::slotLineEditHeapSizeTextChanged(const QString &text)
{
    if (!text.isEmpty())
    {
        Project.setLinkerHeapSize(text);
    }
    else
    {
        ui->lineEditHeapSize->setText(Project.linkerHeapSize());
    }
}

void ViewConfigure::slotLineEditStackSizeTextChanged(const QString &text)
{
    if (!text.isEmpty())
    {
        Project.setLinkerStackSize(text);
    }
    else
    {
        ui->lineEditStackSize->setText(Project.linkerStackSize());
    }
}