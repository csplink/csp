/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        mainwindow_view.cpp
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
#include <QDebug>
#include <QMutex>
#include <QStandardItem>

#include "chip_summary_table.h"
#include "config.h"
#include "mainwindow_view.h"
#include "os.h"
#include "ui_mainwindow_view.h"
#include "wizard_new_project.h"
#include "xmake.h"

static mainwindow_view *mainwindow = nullptr;

void mainwindow_view::sys_message_log_handler(const QtMsgType type, const QMessageLogContext &context,
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
    const QString str_message = QString("%1 %2:%3").arg(str_date_time).arg(strMsg).arg(local_msg.constData());

    if (mainwindow)
    {
        emit mainwindow->signal_add_sys_log(str_message);
    }
    else
    {
        // do nothing
    }
}

void mainwindow_view::xmake_message_log_handler(const QString &msg)
{
    static QMutex mutex;
    QMutexLocker locker(&mutex);

    if (mainwindow)
    {
        emit mainwindow->signal_add_xmake_log(msg);
    }
    else
    {
        // do nothing
    }
}

mainwindow_view::mainwindow_view(QWidget *parent) : QMainWindow(parent), ui(new Ui::mainwindow_view)
{
    ui->setupUi(this);
    mainwindow = this;
    qInstallMessageHandler(mainwindow_view::sys_message_log_handler);
    xmake::install_log_handler(mainwindow_view::xmake_message_log_handler);

    tabifyDockWidget(ui->dockwidget_bottom_output, ui->dockwidget_bottom_xmake_output);
    tabifyDockWidget(ui->dockwidget_bottom_output, ui->dockwidget_bottom_configurations);
    ui->dockwidget_bottom_output->raise();

    _project_instance = project::get_instance();
    ui->page_chip_configure_view->set_propertybrowser(ui->treepropertybrowser);

    connect(ui->action_new_chip, &QAction::triggered, this, &mainwindow_view::action_new_chip_triggered_callback,
            Qt::UniqueConnection);
    connect(ui->action_load, &QAction::triggered, this, &mainwindow_view::action_load_triggered_callback,
            Qt::UniqueConnection);
    connect(ui->action_save, &QAction::triggered, this, &mainwindow_view::action_save_triggered_callback,
            Qt::UniqueConnection);
    connect(ui->action_saveas, &QAction::triggered, this, &mainwindow_view::action_saveas_triggered_callback,
            Qt::UniqueConnection);
    connect(ui->action_close, &QAction::triggered, this, &mainwindow_view::action_close_triggered_callback,
            Qt::UniqueConnection);
    connect(ui->action_report, &QAction::triggered, this, &mainwindow_view::action_report_triggered_callback,
            Qt::UniqueConnection);
    connect(ui->action_generate, &QAction::triggered, this, &mainwindow_view::action_generate_triggered_callback,
            Qt::UniqueConnection);

    connect(ui->page_home_view, &home_view::signal_create_project, this, &mainwindow_view::create_project,
            Qt::UniqueConnection);

    connect(this, &mainwindow_view::signal_add_sys_log, ui->logviewbox_output, &logviewbox::append_data);
    connect(this, &mainwindow_view::signal_add_xmake_log, ui->logviewbox_xmake_output, &logviewbox::append_data);

    init_mode();
}

mainwindow_view::~mainwindow_view()
{
    mainwindow = nullptr;
    delete ui;
}

void mainwindow_view::init_mode()
{
    if (_project_instance->get_core(project::CORE_ATTRIBUTE_TYPE_TYPE) == "chip")
    {
        set_mode(STACK_INDEX_CHIP_CONFIGURE);
    }
    else
    {
        set_mode(STACK_INDEX_HOME);
    }
}

void mainwindow_view::set_mode(const int index)
{
    switch (index)
    {
    case STACK_INDEX_HOME: {
        ui->dockwidget_left->hide();
        ui->dockwidget_right->hide();
        ui->dockwidget_bottom_output->hide();
        ui->dockwidget_bottom_xmake_output->hide();
        ui->dockwidget_bottom_configurations->hide();
        ui->stackedwidget->setCurrentIndex(STACK_INDEX_HOME);
        break;
    }
    case STACK_INDEX_CHIP_CONFIGURE: {
        ui->stackedwidget->setCurrentIndex(STACK_INDEX_CHIP_CONFIGURE);
        ui->dockwidget_left->show();
        ui->dockwidget_right->show();
        ui->dockwidget_bottom_output->show();
        ui->dockwidget_bottom_xmake_output->show();
        ui->dockwidget_bottom_configurations->show();

        connect(ui->page_chip_configure_view, &chip_configure_view::signal_update_modules_treeview, this,
                &mainwindow_view::update_modules_treeview, Qt::UniqueConnection);

        update_modules_treeview(_project_instance->get_core(project::CORE_ATTRIBUTE_TYPE_COMPANY),
                                _project_instance->get_core(project::CORE_ATTRIBUTE_TYPE_TARGET));

        ui->page_chip_configure_view->init_view();

        this->setWindowState(Qt::WindowMaximized);
        break;
    }
    default: {
        break;
    }
    }
}

void mainwindow_view::update_modules_treeview(const QString &company, const QString &name) const
{
    ui->treeview->header()->hide();
    auto *model = new QStandardItemModel(ui->treeview);
    chip_summary_table::chip_summary_t chip_summary;
    chip_summary_table::load_chip_summary(&chip_summary, company, name);
    const auto modules = &chip_summary.modules;
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
    delete ui->treeview->model();
    ui->treeview->setModel(model);
    ui->treeview->expandAll();
}

void mainwindow_view::create_project()
{
    init_mode();
}

void mainwindow_view::action_new_chip_triggered_callback(const bool checked) const
{
    ui->page_home_view->button_create_chip_project_clicked_callback(checked);
}

void mainwindow_view::action_load_triggered_callback(const bool checked)
{
    Q_UNUSED(checked)

    const auto file = os::getexistfile();
    if (file.isEmpty())
        return;
    try
    {
        _project_instance->load_project(file);
        init_mode();
    }
    catch (const std::exception &e)
    {
        os::show_error(tr("Project load failed, reason: <%1>.").arg(e.what()));
    }
}

void mainwindow_view::action_save_triggered_callback(const bool checked)
{
    Q_UNUSED(checked)

    if (_project_instance->get_path().isEmpty())
    {
        wizard_new_project wizard(this);
        connect(&wizard, &wizard_new_project::finished, this, [this](const int result) {
            if (result == QDialog::Accepted)
            {
                _project_instance->save_project();
            }
        });
        wizard.exec();
    }
    else
    {
        _project_instance->save_project();
    }
}

void mainwindow_view::action_saveas_triggered_callback(const bool checked) const
{
    Q_UNUSED(checked)
}

void mainwindow_view::action_close_triggered_callback(const bool checked) const
{
    Q_UNUSED(checked)
}

void mainwindow_view::action_report_triggered_callback(const bool checked) const
{
    Q_UNUSED(checked)
}

void mainwindow_view::action_generate_triggered_callback(const bool checked) const
{
    Q_UNUSED(checked)

    _project_instance->generate_code("xmake");
}
