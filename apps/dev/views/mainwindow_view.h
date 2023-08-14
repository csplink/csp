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
namespace Ui {
class mainwindow_view;
}
QT_END_NAMESPACE

class mainwindow_view : public QMainWindow {
    Q_OBJECT

private:
    typedef enum
    {
        STACK_INDEX_HOME = 0,
        STACK_INDEX_CHIP_CONFIGURE
    } stack_index_type;

public:
    explicit mainwindow_view(QWidget *parent = nullptr);
    ~mainwindow_view() override;

private:
    void init_mode();
    void set_mode(stack_index_type index);

public slots:
    void update_modules_treeview(const QString &company, const QString &name);
    void create_project();

private slots:
    void action_new_chip_triggered_callback(bool checked);
    void action_load_triggered_callback(bool checked);
    void action_save_triggered_callback(bool checked);
    void action_saveas_triggered_callback(bool checked);
    void action_close_triggered_callback(bool checked);
    void action_report_triggered_callback(bool checked);
    void action_generate_triggered_callback(bool checked);

private:
    Ui::mainwindow_view *ui;
    project             *_project_instance;
};
#endif  // MAINWINDOW_VIEW_H
