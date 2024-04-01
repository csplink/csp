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
#include <QMutex>

#include "ChipSummaryTable.h"
#include "DialogPackageManager.h"
#include "ViewMainWindow.h"
#include "WizardNewProject.h"
#include "ui_ViewMainWindow.h"

static ViewMainWindow *mainWindow = nullptr;

void ViewMainWindow::sysMessageLogHandler(const QtMsgType type, const QMessageLogContext &context,
                                          const QString &msg)
{
    Q_UNUSED(context);

    static QMutex mutex;
    QMutexLocker locker(&mutex);
    const QByteArray local_msg = msg.toLocal8Bit();

    QString strMsg("");
    switch (type)
    {
    case QtDebugMsg:
        strMsg = QString("Debug:");
        break;
    case QtInfoMsg:
        strMsg = QString("Info:");
        break;
    case QtWarningMsg:
        strMsg = QString("Warning:");
        break;
    case QtCriticalMsg:
        strMsg = QString("Critical:");
        break;
    case QtFatalMsg:
        strMsg = QString("Fatal:");
        break;

    default:
        break;
    }

    const QString str_date_time = QDateTime::currentDateTime().toString("hh:mm:ss");
    const QString str_message = QString("%1 %2:%3").arg(str_date_time, strMsg, local_msg.constData());

    if (mainWindow != nullptr)
    {
        emit mainWindow->signalAddLog(str_message);
    }
    else
    {
        // do nothing
    }
}

void ViewMainWindow::messageLogHandler(const QString &msg)
{
    static QMutex mutex;
    QMutexLocker locker(&mutex);

    if (mainWindow != nullptr)
    {
        emit mainWindow->signalAddLog(msg);
    }
    else
    {
        // do nothing
    }
}

ViewMainWindow::ViewMainWindow(QWidget *parent)
    : QMainWindow(parent), ui_(new Ui::viewMainWindow)
{
    ui_->setupUi(this);
    mainWindow = this;
    (void)qInstallMessageHandler(ViewMainWindow::sysMessageLogHandler);

    tabifyDockWidget(ui_->dockWidgetBottomOutput, ui_->dockWidgetBottomConfigurations);
    ui_->dockWidgetBottomOutput->raise();

    projectInstance_ = Project::getInstance();
    XMakeAsync *xmake = XMakeAsync::getInstance();
    ui_->pageViewConfigure->setPropertyBrowser(ui_->treePropertyBrowser);

    (void)connect(ui_->actionNewChip, &QAction::triggered, this, &ViewMainWindow::actionNewChipTriggeredCallback, Qt::UniqueConnection);
    (void)connect(ui_->actionLoad, &QAction::triggered, this, &ViewMainWindow::actionLoadTriggeredCallback, Qt::UniqueConnection);
    (void)connect(ui_->actionSave, &QAction::triggered, this, &ViewMainWindow::actionSaveTriggeredCallback, Qt::UniqueConnection);
    (void)connect(ui_->actionSaveAs, &QAction::triggered, this, &ViewMainWindow::actionSaveAsTriggeredCallback, Qt::UniqueConnection);
    (void)connect(ui_->actionClose, &QAction::triggered, this, &ViewMainWindow::actionCloseTriggeredCallback, Qt::UniqueConnection);
    (void)connect(ui_->actionReport, &QAction::triggered, this, &ViewMainWindow::actionReportTriggeredCallback, Qt::UniqueConnection);
    (void)connect(ui_->actionGenerate, &QAction::triggered, this, &ViewMainWindow::actionGenerateTriggeredCallback, Qt::UniqueConnection);
    (void)connect(ui_->actionPackageManager, &QAction::triggered, this, &ViewMainWindow::actionPackageManagerTriggeredCallback, Qt::UniqueConnection);
    (void)connect(ui_->actionBuildDebug, &QAction::triggered, this, &ViewMainWindow::actionBuildDebugTriggeredCallback, Qt::UniqueConnection);
    (void)connect(ui_->actionBuildRelease, &QAction::triggered, this, &ViewMainWindow::actionBuildReleaseTriggeredCallback, Qt::UniqueConnection);

    (void)connect(xmake, &XMakeAsync::signalReadyReadStandardOutput, this, &ViewMainWindow::xmakeReadyReadStandardOutputCallback, Qt::UniqueConnection);

    (void)connect(ui_->pageViewHome, &ViewHome::signalCreateProject, this, &ViewMainWindow::createProject, Qt::UniqueConnection);
    (void)connect(this, &ViewMainWindow::signalAddLog, ui_->LogBoxOutput, &LogBox::append, Qt::UniqueConnection);

    (void)connect(ui_->pageViewHome, &ViewHome::signalOpenExistingProject, this, &ViewMainWindow::actionLoadTriggeredCallback, Qt::UniqueConnection);
    (void)connect(projectInstance_, &Project::signalsLog, ui_->LogBoxOutput, &LogBox::append, Qt::UniqueConnection);

    initMode();
}

ViewMainWindow::~ViewMainWindow()
{
    mainWindow = nullptr;
    delete ui_;
}

void ViewMainWindow::initMode()
{
    if (projectInstance_->getProjectType() == "chip")
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
        ui_->dockWidgetLeft->hide();
        ui_->dockWidgetRight->hide();
        ui_->dockWidgetBottomOutput->hide();
        ui_->dockWidgetBottomConfigurations->hide();
        ui_->stackedWidget->setCurrentIndex(STACK_INDEX_HOME);
        ui_->menuBar->hide();
        ui_->toolBar->hide();
        ui_->statusBar->hide();
        break;
    }
    case STACK_INDEX_CHIP_CONFIGURE: {
        ui_->menuBar->show();
        ui_->toolBar->show();
        ui_->statusBar->show();
        ui_->dockWidgetLeft->show();
        ui_->dockWidgetRight->show();
        ui_->dockWidgetBottomOutput->show();
        ui_->dockWidgetBottomConfigurations->show();

        (void)connect(ui_->pageViewConfigure, &ViewConfigure::signalUpdateModulesTreeView, this,
                      &ViewMainWindow::updateModulesTreeView, Qt::UniqueConnection);

        updateModulesTreeView(projectInstance_->getProjectCompany(), projectInstance_->getProjectTargetChip());

        ui_->pageViewConfigure->initView();
        ui_->stackedWidget->setCurrentIndex(STACK_INDEX_CHIP_CONFIGURE);

        this->setWindowState(Qt::WindowMaximized);
        break;
    }
    case STACK_INDEX_EMPTY: {
        ui_->stackedWidget->setCurrentIndex(STACK_INDEX_EMPTY);
        ui_->menuBar->show();
        ui_->toolBar->show();
        ui_->statusBar->show();
        ui_->dockWidgetLeft->show();
        ui_->dockWidgetRight->show();
        ui_->dockWidgetBottomOutput->show();
        ui_->dockWidgetBottomConfigurations->show();
        this->setWindowState(Qt::WindowMaximized);
        break;
    }
    default: {
        break;
    }
    }
}

void ViewMainWindow::updateModulesTreeView(const QString &company, const QString &name) const
{
    ui_->treeView->header()->hide();
    auto *model = new QStandardItemModel(ui_->treeView);
    ChipSummaryTable::ChipSummaryType chip_summary;
    ChipSummaryTable::loadChipSummary(&chip_summary, company, name);
    const auto modules = &chip_summary.Modules;
    auto modules_i = modules->constBegin();
    while (modules_i != modules->constEnd())
    {
        const auto item = new QStandardItem(modules_i.key());
        item->setEditable(false);
        model->appendRow(item);

        const auto module = &modules_i.value();
        auto module_i = module->constBegin();
        while (module_i != module->constEnd())
        {
            const auto item_child = new QStandardItem(module_i.key());
            item_child->setEditable(false);
            item->appendRow(item_child);
            ++module_i;
        }
        ++modules_i;
    }
    delete ui_->treeView->model();
    ui_->treeView->setModel(model);
    ui_->treeView->expandAll();
}

void ViewMainWindow::createProject()
{
    initMode();
}

void ViewMainWindow::actionNewChipTriggeredCallback(const bool checked) const
{
    ui_->pageViewHome->pushButtonCreateChipProjectClickedCallback(checked);
}

void ViewMainWindow::actionLoadTriggeredCallback(const bool checked)
{
    Q_UNUSED(checked)

    const auto file = QFileDialog::getOpenFileName(nullptr, QString(), QString(), tr("CSP project file(*.csp)"), nullptr);
    if (!file.isEmpty())
    {
        try
        {
            projectInstance_->loadProject(file);
            initMode();
        }
        catch (const std::exception &e)
        {
            qCritical() << tr("Project load failed, reason: <%1>.").arg(e.what());
        }
    }
}

void ViewMainWindow::actionSaveTriggeredCallback(const bool checked)
{
    Q_UNUSED(checked)

    if (projectInstance_->getPath().isEmpty())
    {
        WizardNewProject wizard(this);
        (void)connect(&wizard, &WizardNewProject::finished, this, [this](const int result) {
            if (result == QDialog::Accepted)
            {
                projectInstance_->saveProject();
            }
        });
        (void)wizard.exec();
    }
    else
    {
        projectInstance_->saveProject();
    }
}

void ViewMainWindow::actionSaveAsTriggeredCallback(const bool checked) const
{
    Q_UNUSED(checked)
}

void ViewMainWindow::actionCloseTriggeredCallback(const bool checked) const
{
    Q_UNUSED(checked)
}

void ViewMainWindow::actionReportTriggeredCallback(const bool checked) const
{
    Q_UNUSED(checked)
}

void ViewMainWindow::actionGenerateTriggeredCallback(const bool checked) const
{
    Q_UNUSED(checked)
    ui_->dockWidgetBottomOutput->raise();
    projectInstance_->saveProject();
    projectInstance_->generateCode();
}

void ViewMainWindow::actionPackageManagerTriggeredCallback(const bool checked)
{
    Q_UNUSED(checked)

    DialogPackageManager dialog(this);
    (void)dialog.exec();
}

void ViewMainWindow::actionBuildDebugTriggeredCallback(bool checked) const
{
    Q_UNUSED(checked)

    projectInstance_->build("debug");
}

void ViewMainWindow::actionBuildReleaseTriggeredCallback(bool checked) const
{
    Q_UNUSED(checked)

    projectInstance_->build("release");
}

void ViewMainWindow::xmakeReadyReadStandardOutputCallback(const QProcess *process, const QString &msg)
{
    Q_UNUSED(process);
    ui_->LogBoxOutput->append(msg);
}
