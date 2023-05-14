/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        mcu_configure_view.h
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

#ifndef MCU_CONFIGURE_VIEW_H
#define MCU_CONFIGURE_VIEW_H

#include <QWidget>

namespace Ui {
class mcu_configure_view;
}

class mcu_configure_view : public QWidget {
    Q_OBJECT

public:
    explicit mcu_configure_view(QWidget *parent = nullptr);
    ~mcu_configure_view() override;

private:
    Ui::mcu_configure_view *ui;
};

#endif  // MCU_CONFIGURE_VIEW_H
