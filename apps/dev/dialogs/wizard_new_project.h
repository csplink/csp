/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        wizard_new_project.h
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
 *  2023-05-29     xqyjlj       initial version
 */

#ifndef WIZARD_NEW_PROJECT_H
#define WIZARD_NEW_PROJECT_H

#include <QLabel>
#include <QLineEdit>
#include <QWizard>

#include "project.h"

class wizard_new_project : public QWizard {
    Q_OBJECT

public:
    explicit wizard_new_project(QWidget *parent);

    void accept() override;

private:
    QLineEdit *lineedit_project_path = nullptr;
    QLineEdit *lineedit_project_name = nullptr;

private:
    project     *_project_instance = nullptr;
    QWizardPage *create_page_introduce();
    QWizardPage *create_page_choose_path();
};

#endif  // WIZARD_NEW_PROJECT_H
