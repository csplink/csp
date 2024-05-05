/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ViewMainWindow.cpp
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

#include <QDateTime>
#include <QFileDialog>
#include <QMessageBox>
#include <QMutex>

#include "DialogPackageManager.h"
#include "Settings.h"
#include "ViewMainWindow.h"
#include "WizardNewProject.h"
#include "ui_ViewMainWindow.h"

ViewMainWindow::ViewMainWindow(QWidget *parent)
    : QMainWindow(parent),
      ui(new Ui::viewMainWindow),
      m_dockLog(nullptr),
      m_dockPropertyBrowserPin(nullptr),
      m_dockModuleTree(nullptr)
{
    ui->setupUi(this);
    {
        m_dockLog = new DockLog(this);
        m_dockLog->hide();
        addDockWidget(Qt::BottomDockWidgetArea, m_dockLog);
        m_dockLog->setVisible(true);

        m_dockPropertyBrowserPin = new DockPropertyBrowserPin(this);
        m_dockPropertyBrowserPin->hide();
        addDockWidget(Qt::RightDockWidgetArea, m_dockPropertyBrowserPin);
        m_dockPropertyBrowserPin->setVisible(true);

        m_dockModuleTree = new DockModuleTree(this);
        m_dockModuleTree->hide();
        addDockWidget(Qt::LeftDockWidgetArea, m_dockModuleTree);
        m_dockModuleTree->setVisible(true);
    }
    //    tabifyDockWidget(ui_->dockWidgetBottomOutput, ui_->dockWidgetBottomConfigurations);
    //    ui_->dockWidgetBottomOutput->raise();

    ui->pageViewConfigure->setPropertyBrowser(m_dockPropertyBrowserPin->propertyBrowser());

    {
        (void)connect(ui->actionNewChip, &QAction::triggered, this, &ViewMainWindow::slotActionNewChipTriggered);
        (void)connect(ui->actionLoad, &QAction::triggered, this, &ViewMainWindow::slotActionLoadTriggered);
        (void)connect(ui->actionSave, &QAction::triggered, this, &ViewMainWindow::slotActionSaveTriggered);
        (void)connect(ui->actionSaveAs, &QAction::triggered, this, &ViewMainWindow::slotActionSaveAsTriggered);
        (void)connect(ui->actionClose, &QAction::triggered, this, &ViewMainWindow::slotActionCloseTriggered);
        (void)connect(ui->actionReport, &QAction::triggered, this, &ViewMainWindow::slotActionReportTriggered);
        (void)connect(ui->actionGenerate, &QAction::triggered, this, &ViewMainWindow::slotActionGenerateTriggered);
        (void)connect(ui->actionPackageManager, &QAction::triggered, this,
                      &ViewMainWindow::slotActionPackageManagerTriggered);
        (void)connect(ui->actionAboutQt, &QAction::triggered, qApp, &QApplication::aboutQt);
    }

    (void)connect(ui->pageViewHome, &ViewHome::signalCreateProject, this, &ViewMainWindow::createProject);
    //    (void)connect(this, &ViewMainWindow::signalAddLog, ui_->LogBoxOutput, &LogBox::append);

    (void)connect(ui->pageViewHome, &ViewHome::signalOpenExistingProject, this,
                  &ViewMainWindow::slotActionLoadTriggered);
    //    (void)connect(projectInstance_, &Project::signalsLog, ui_->LogBoxOutput, &LogBox::append);

    (void)connect(ui->pageViewConfigure, &ViewConfigure::signalUpdateModulesTreeView, m_dockModuleTree,
                  QOverload<const QString &, const QString &>::of(&DockModuleTree::setModule));

    initMode();

    this->setWindowState(Qt::WindowMaximized);
}

ViewMainWindow::~ViewMainWindow()
{
    delete ui;
}

void ViewMainWindow::initMode()
{
    if (Project.type() == "chip")
    {
        setMode(STACK_INDEX_EMPTY);
        setMode(STACK_INDEX_CHIP_CONFIGURE);
    }
    else
    {
        setMode(STACK_INDEX_HOME);
    }
}

void ViewMainWindow::setMode(const StackIndexType index)
{
    switch (index)
    {
    case STACK_INDEX_HOME: {
        ui->stackedWidget->setCurrentIndex(STACK_INDEX_HOME);
        break;
    }
    case STACK_INDEX_CHIP_CONFIGURE: {
        ui->stackedWidget->setCurrentIndex(STACK_INDEX_CHIP_CONFIGURE);
        m_dockModuleTree->setModule(Project.company(), Project.targetChip());
        break;
    }
    case STACK_INDEX_EMPTY: {
        ui->stackedWidget->setCurrentIndex(STACK_INDEX_EMPTY);
        break;
    }
    default: {
        break;
    }
    }
}

void ViewMainWindow::createProject()
{
    initMode();
}

void ViewMainWindow::slotActionNewChipTriggered() const
{
    ui->pageViewHome->pushButtonCreateChipProjectClickedCallback(true);
}

void ViewMainWindow::slotActionLoadTriggered()
{
    const auto file = QFileDialog::getOpenFileName(this, QString(), Settings.openPath(), tr("CSP project file(*.csp)"));
    if (!file.isEmpty())
    {
        Settings.setOpenPath(QFileInfo(file).path());
        try
        {
            Project.loadProject(file);
            initMode();
        }
        catch (const std::exception &e)
        {
            qCritical() << tr("Project load failed, reason: <%1>.").arg(e.what());
        }
    }
}

void ViewMainWindow::slotActionSaveTriggered()
{
    if (Project.path().isEmpty())
    {
        WizardNewProject wizard(this);
        (void)connect(&wizard, &WizardNewProject::finished, this, [](const int result) {
            if (result == QDialog::Accepted)
            {
                Project.saveProject();
            }
        });
        (void)wizard.exec();
    }
    else
    {
        Project.saveProject();
    }
}

void ViewMainWindow::slotActionSaveAsTriggered() const
{
}

void ViewMainWindow::slotActionCloseTriggered() const
{
}

void ViewMainWindow::slotActionReportTriggered() const
{
}

void ViewMainWindow::slotActionGenerateTriggered() const
{
    //    ui_->dockWidgetBottomOutput->raise();
    Project.saveProject();
    Project.generateCode();
}

void ViewMainWindow::slotActionPackageManagerTriggered()
{
    DialogPackageManager dialog(this);
    (void)dialog.exec();
}
