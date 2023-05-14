/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        choose_mcu_dialog.h
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
 *  2023-05-13     xqyjlj       initial version
 */

#ifndef CHOOSE_MCU_DIALOG_H
#define CHOOSE_MCU_DIALOG_H

#include <QDialog>

namespace Ui {
class choose_mcu_dialog;
}

class choose_mcu_dialog : public QDialog {
    Q_OBJECT

public:
    explicit choose_mcu_dialog(QWidget *parent = nullptr);
    ~choose_mcu_dialog() override;

private:
    Ui::choose_mcu_dialog *ui;
};

#endif  // CHOOSE_MCU_DIALOG_H
