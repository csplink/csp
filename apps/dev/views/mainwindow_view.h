/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        mainwindow_view.h
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

#ifndef MAINWINDOW_VIEW_H
#define MAINWINDOW_VIEW_H

#include <QMainWindow>

#include "project.h"

QT_BEGIN_NAMESPACE
namespace Ui
{
class mainwindow_view;
}
QT_END_NAMESPACE

class mainwindow_view final : public QMainWindow
{
    Q_OBJECT

  private:
    typedef enum
    {
        STACK_INDEX_HOME,
        STACK_INDEX_CHIP_CONFIGURE,
        STACK_INDEX_EMPTY,
    } stack_index_type;

  public:
    explicit mainwindow_view(QWidget *parent = nullptr);
    virtual ~mainwindow_view() override;

  signals:
    void signal_add_sys_log(const QString &string);
    void signal_add_xmake_log(const QString &string);

  private:
    void init_mode();
    void set_mode(int index);
    static void sys_message_log_handler(QtMsgType type, const QMessageLogContext &context, const QString &msg);
    static void xmake_message_log_handler(const QString &msg);

  public slots:
    void update_modules_treeview(const QString &company, const QString &name) const;
    void create_project();

  private slots:
    void action_new_chip_triggered_callback(bool checked) const;
    void action_load_triggered_callback(bool checked);
    void action_save_triggered_callback(bool checked);
    void action_saveas_triggered_callback(bool checked) const;
    void action_close_triggered_callback(bool checked) const;
    void action_report_triggered_callback(bool checked) const;
    void action_generate_triggered_callback(bool checked) const;
    void action_package_manager_triggered_callback(bool checked);

  private:
    Ui::mainwindow_view *_ui;
    project *_project_instance;
};
#endif // MAINWINDOW_VIEW_H
