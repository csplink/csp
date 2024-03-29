/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        WizardNewProject.cpp
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
#include <QDir>
#include <QFileDialog>
#include <QLabel>
#include <QToolButton>
#include <QVBoxLayout>

#include "Config.h"
#include "WizardNewProject.h"

WizardNewProject::WizardNewProject(const QWidget *parent)
{
    Q_UNUSED(parent)

    projectInstance_ = Project::getInstance();

    setWindowTitle(tr("New Project"));
    setWindowFlags(Qt::Dialog | Qt::WindowCloseButtonHint | Qt::WindowMinimizeButtonHint |
                   Qt::WindowMaximizeButtonHint);

    setButtonText(NextButton, tr("Next"));
    setButtonText(BackButton, tr("Back"));
    setButtonText(FinishButton, tr("Finish"));
    setButtonText(CancelButton, tr("Cancel"));

    addPage(createPageIntroduce());
    addPage(createPageChoosePath());
}

void WizardNewProject::accept()
{
    auto path = lineEditProjectPath_->text();
    auto name = lineEditProjectName_->text();

    if (path.isEmpty() || name.isEmpty())
    {
        qWarning().noquote() << tr("Please input project path and name");
        return;
    }

    projectInstance_->setPath(QString("%1/%2/%2.csp").arg(path, name));
    projectInstance_->setName(name);

    QDialog::accept();
}

QWizardPage *WizardNewProject::createPageIntroduce()
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

QWizardPage *WizardNewProject::createPageChoosePath()
{
    auto *page = new QWizardPage(this);

    const auto label1 = new QLabel(tr("Project Path"), page);
    label1->setWordWrap(true);

    const auto label2 = new QLabel(tr("Project Name"), page);
    label2->setWordWrap(true);

    auto workspace = Config::workspaceDir();
    lineEditProjectPath_ = new QLineEdit(workspace, page);

    int index = 0;

    while (1)
    {
        const QDir dir(QString("%1/untitled%2").arg(workspace, index == 0 ? "" : QString::number(index)));
        if (dir.exists())
        {
            index++;
        }
        else
        {
            break;
        }
    }
    lineEditProjectName_ = new QLineEdit(QString("untitled%1").arg(index == 0 ? "" : QString::number(index)), page);

    const auto toolButton = new QToolButton(page);
    toolButton->setMaximumSize(30, 30);
    toolButton->setText("...");

    const auto gridLayout = new QGridLayout(page);

    gridLayout->addWidget(label1, 0, 0, 1, 1);
    gridLayout->addWidget(lineEditProjectPath_, 0, 1, 1, 1);
    gridLayout->addWidget(toolButton, 0, 2, 1, 1);
    gridLayout->addWidget(label2, 1, 0, 1, 1);
    gridLayout->addWidget(lineEditProjectName_, 1, 1, 1, 1);

    page->setLayout(gridLayout);

    connect(toolButton, &QToolButton::pressed, this, [this]() {
        const QString path = QFileDialog::getExistingDirectory();
        if (!path.isEmpty())
        {
            lineEditProjectPath_->setText(path);
        }
    });

    return page;
}
