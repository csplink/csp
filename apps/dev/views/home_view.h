/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        home_view.h
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

#ifndef HOME_VIEW_H
#define HOME_VIEW_H

#include <QWidget>

#include "project.h"

namespace Ui
{
class home_view;
}

class home_view final : public QWidget
{
    Q_OBJECT

  public:
    explicit home_view(QWidget *parent = nullptr);
    virtual ~home_view() override;

  signals:
    void signal_create_project();
    void signal_open_existing_project(bool checked);

  public slots:
    void button_create_chip_project_clicked_callback(bool checked);
    void create_chip_project();

  private slots:
    void button_create_board_project_clicked_callback(bool checked);
    void choose_chip_dialog_finished_callback(int result);
    void button_open_existing_project_clicked_callback(bool checked);

  private:
    Ui::home_view *ui;

    project *_project_instance;
};

#endif // HOME_VIEW_H
