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

#include <QFileDialog>
#include <QLabel>
#include <QToolButton>
#include <QVBoxLayout>

#include "Project.h"
#include "Settings.h"
#include "WizardNewProject.h"

WizardNewProject::WizardNewProject(QWidget *parent)
    : QWizard(parent),
      m_lineEditProjectPath(nullptr),
      m_lineEditProjectName(nullptr)
{
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
    auto path = m_lineEditProjectPath->text();
    auto name = m_lineEditProjectName->text();

    if (path.isEmpty() || name.isEmpty())
    {
        qWarning().noquote() << tr("Please input project path and name");
        return;
    }

    Project.setPath(QString("%1/%2/%2.csp").arg(path, name));
    Project.setName(name);

    QDialog::accept();
}

QWizardPage *WizardNewProject::createPageIntroduce()
{
    QWizardPage *page = new QWizardPage(this);
    page->setTitle(tr("Welcome to use this wizard to create a new project"));

    QLabel *label1 = new QLabel(tr("this will create a new project in the path you choose."), this);
    label1->setWordWrap(true);

    QLabel *label2 = new QLabel(tr("Click Next to continue, or Cancel to exit Setup."), this);
    label2->setWordWrap(true);

    QVBoxLayout *layout = new QVBoxLayout(this);
    layout->addWidget(label1);
    layout->addWidget(label2);
    page->setLayout(layout);

    return page;
}

QWizardPage *WizardNewProject::createPageChoosePath()
{
    QWizardPage *page = new QWizardPage(this);

    QLabel *label1 = new QLabel(tr("Project Path"), page);
    label1->setWordWrap(true);

    QLabel *label2 = new QLabel(tr("Project Name"), page);
    label2->setWordWrap(true);

    QString workspace = Settings.workspace();
    m_lineEditProjectPath = new QLineEdit(workspace, page);

    int index = 0;

    while (true)
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
    m_lineEditProjectName = new QLineEdit(QString("untitled%1").arg(index == 0 ? "" : QString::number(index)), page);

    QToolButton *toolButton = new QToolButton(page);
    toolButton->setMaximumSize(30, 30);
    toolButton->setText("...");

    QGridLayout *gridLayout = new QGridLayout(page);

    gridLayout->addWidget(label1, 0, 0, 1, 1);
    gridLayout->addWidget(m_lineEditProjectPath, 0, 1, 1, 1);
    gridLayout->addWidget(toolButton, 0, 2, 1, 1);
    gridLayout->addWidget(label2, 1, 0, 1, 1);
    gridLayout->addWidget(m_lineEditProjectName, 1, 1, 1, 1);

    page->setLayout(gridLayout);

    connect(toolButton, &QToolButton::pressed, this, [this]() {
        const QString path = QFileDialog::getExistingDirectory();
        if (!path.isEmpty())
        {
            m_lineEditProjectPath->setText(path);
        }
    });

    return page;
}
