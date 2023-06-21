/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        wizard_new_project.cpp
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

#include <QDebug>
#include <QToolButton>
#include <QVBoxLayout>

#include "os.h"
#include "wizard_new_project.h"

wizard_new_project::wizard_new_project(QWidget *parent)
{
    Q_UNUSED(parent);

    _project_instance = project::get_instance();

    setWindowTitle(tr("New Project"));
    setWindowFlags(Qt::Dialog | Qt::WindowCloseButtonHint | Qt::WindowMinimizeButtonHint |
                   Qt::WindowMaximizeButtonHint);

    setButtonText(QWizard::NextButton, tr("Next"));
    setButtonText(QWizard::BackButton, tr("Back"));
    setButtonText(QWizard::FinishButton, tr("Finish"));
    setButtonText(QWizard::CancelButton, tr("Cancel"));

    addPage(create_page_introduce());
    addPage(create_page_choose_path());
}

void wizard_new_project::accept()
{
    auto path = lineedit_project_path->text();
    auto name = lineedit_project_name->text();

    if (path.isEmpty() || name.isEmpty())
    {
        os::show_warning(tr("Please input project path and name"));
        return;
    }

    _project_instance->set_path(path);
    _project_instance->set_core(CSP_PROJECT_CORE_NAME, name);

    QDialog::accept();
}

QWizardPage *wizard_new_project::create_page_introduce()
{
    QFont font;
    font.setBold(true);
    font.setPointSize(12);

    auto *page = new QWizardPage(this);
    page->setTitle(tr("Welcome to use this wizard to create a new project"));

    auto *label1 = new QLabel(tr("this will create a new project in the path you choose."), this);
    label1->setWordWrap(true);

    auto *label2 = new QLabel(tr("Click Next to continue, or Cancel to exit Setup."), this);
    label2->setWordWrap(true);

    auto *layout = new QVBoxLayout(this);
    layout->addWidget(label1);
    layout->addWidget(label2);
    page->setLayout(layout);

    return page;
}

QWizardPage *wizard_new_project::create_page_choose_path()
{
    auto *page = new QWizardPage(this);

    auto label1 = new QLabel(tr("Project Path"), page);
    label1->setWordWrap(true);

    auto label2 = new QLabel(tr("Project Name"), page);
    label2->setWordWrap(true);

    lineedit_project_path = new QLineEdit(page);
    lineedit_project_name = new QLineEdit(page);

    auto toolbutton1 = new QToolButton(page);
    toolbutton1->setMaximumSize(30, 30);
    toolbutton1->setText("...");

    auto gridlayout = new QGridLayout(page);

    gridlayout->addWidget(label1, 0, 0, 1, 1);
    gridlayout->addWidget(lineedit_project_path, 0, 1, 1, 1);
    gridlayout->addWidget(toolbutton1, 0, 2, 1, 1);
    gridlayout->addWidget(label2, 1, 0, 1, 1);
    gridlayout->addWidget(lineedit_project_name, 1, 1, 1, 1);

    page->setLayout(gridlayout);

    connect(toolbutton1, &QToolButton::pressed, this, [=]() {
        QString path = os::getexistdir();
        if (!path.isEmpty())
        {
            lineedit_project_path->setText(path);
        }
    });

    return page;
}
