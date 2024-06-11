/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        WizardPackageInstaller.cpp
 * @brief
 *
 *****************************************************************************
 * @attention
 * Licensed under the GNU General Public License v. 3 (the "License");
 * You may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.gnu.org/licenses/gpl-3.0.html
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Copyright (C) 2024-2024 xqyjlj<xqyjlj@126.com>
 *
 *****************************************************************************
 * Change Logs:
 * Date           Author       Notes
 * ------------   ----------   -----------------------------------------------
 * 2024-05-21     xqyjlj       initial version
 */

#include <QCoreApplication>
#include <QFile>
#include <QFileDialog>
#include <QMessageBox>
#include <QVBoxLayout>

#include "Configure.h"
#include "PackageDescriptionTable.h"
#include "PackageManager.h"
#include "Settings.h"
#include "WizardPackageInstaller.h"

WizardPackageInstaller::WizardPackageInstaller(QWidget *parent, const QString &path)
    : QWizard(parent)
{
    setWindowTitle(tr("Package installer"));

    setWizardStyle(ModernStyle);

    setPixmap(QWizard::LogoPixmap,
              QPixmap(":/images/logo.svg").scaled(QSize(64, 64), Qt::KeepAspectRatio, Qt::SmoothTransformation));

    setButtonText(NextButton, tr("Next"));
    setButtonText(BackButton, tr("Back"));
    setButtonText(FinishButton, tr("Finish"));
    setButtonText(CancelButton, tr("Cancel"));
    setButtonText(CommitButton, tr("Start"));
    setOption(HaveHelpButton, true);

    setPage(Page_Intro, new WizardPackageInstallerIntroPage(this, path));
    setPage(Page_Installer, new WizardPackageInstallerStatusPage(this));
    setPage(Page_Result, new WizardPackageInstallerResultPage(this));

    setStartId(Page_Intro);

    connect(this, &QWizard::helpRequested, this, &WizardPackageInstaller::slotSelfShowHelp);
}

void WizardPackageInstaller::accept()
{
    QDialog::accept();
}

void WizardPackageInstaller::slotSelfShowHelp()
{
    static QString lastHelpMessage;

    QString message;

    switch (currentId())
    {
    case Page_Intro:
        message = tr("On this page, select the package you want to install.");
        break;
    default:
        message = tr("This help is likely not to be of any help.");
        break;
    }

    if (lastHelpMessage == message)
    {
        message = tr("Sorry, I already gave what help I could. Maybe you should try asking a human?");
    }

    QMessageBox::information(this, tr("Package Installer"), message);

    lastHelpMessage = message;
}

WizardPackageInstallerIntroPage::WizardPackageInstallerIntroPage(QWidget *parent, const QString &path)
    : QWizardPage(parent),
      m_packagePath(path),
      m_lineEditPackagePath(nullptr),
      m_pushButtonChoosePackagePath(nullptr)
{
    setTitle(tr("Version %1").arg(CONFIGURE_PROJECT_VERSION));
    setSubTitle(tr("This wizard will help install a package"));
    setCommitPage(true);

    QVBoxLayout *layout = new QVBoxLayout(this);
    layout->setSpacing(16);

    {
        QLabel *label = new QLabel(tr("This program installs the Package:"), this);
        label->setWordWrap(true);
        layout->addWidget(label);
    }

    {
        QHBoxLayout *hLayout = new QHBoxLayout(nullptr);
        m_lineEditPackagePath = new QLineEdit(this);
        m_pushButtonChoosePackagePath = new QPushButton(this);

        connect(m_pushButtonChoosePackagePath, &QPushButton::pressed, this, [this]() {
            const QString path = QFileDialog::getOpenFileName(this, tr("Choose Package"), Settings.packagePath(),
                                                              tr("CSP Package File(*.csppkg)"));
            if (!path.isEmpty())
            {
                Settings.setPackagePath(QFileInfo(path).path());
                m_lineEditPackagePath->setText(path);
            }
        });

        registerField("introduction.packagePath*", m_lineEditPackagePath);

        QIcon icon;
        icon.addFile(QString::fromUtf8(":/icons/32x32/more-line.svg"), QSize(), QIcon::Normal, QIcon::Off);
        m_pushButtonChoosePackagePath->setIcon(icon);
        m_lineEditPackagePath->setReadOnly(true);
        hLayout->addWidget(m_lineEditPackagePath);
        hLayout->addWidget(m_pushButtonChoosePackagePath);
        layout->addLayout(hLayout);
    }

    {
        QLabel *label = new QLabel(tr("To"), this);
        label->setWordWrap(true);
        layout->addWidget(label);
    }

    {
        QLineEdit *lineEdit = new QLineEdit(Settings.repository(), this);
        lineEdit->setReadOnly(true);
        lineEdit->setEnabled(false);
        layout->addWidget(lineEdit);
    }

    {
        QLabel *label = new QLabel(tr("Click Next to continue, or Cancel to exit Setup."), this);
        label->setWordWrap(true);
        layout->addWidget(label);
    }

    setLayout(layout);
}

void WizardPackageInstallerIntroPage::initializePage()
{
    if (!m_packagePath.isEmpty() && QFile::exists(m_packagePath) && m_packagePath.endsWith(".csppkg"))
    {
        m_lineEditPackagePath->setText(m_packagePath);
        m_pushButtonChoosePackagePath->setEnabled(false);
    }
}

int WizardPackageInstallerIntroPage::nextId() const
{
    return WizardPackageInstaller::Page_Installer;
}

WizardPackageInstallerStatusPage::WizardPackageInstallerStatusPage(QWidget *parent)
    : QWizardPage(parent),
      m_isFinish(false),
      m_packagePath(),
      m_labelPackagePath(nullptr),
      m_isInit(false)
{
    setTitle(tr("Install Status"));
    setSubTitle(tr("install package"));

    QVBoxLayout *layout = new QVBoxLayout(this);
    layout->setSpacing(16);

    {
        QLabel *label = new QLabel(tr("install package ..."), this);
        label->setWordWrap(true);
        layout->addWidget(label);
    }

    {
        m_labelPackagePath = new QLabel(m_packagePath, this);
        m_labelPackagePath->setWordWrap(true);
        layout->addWidget(m_labelPackagePath);
    }

    {
        m_progressBar = new QProgressBar(this);
        m_progressBar->setRange(0, 100);
        m_progressBar->setValue(0);
        layout->addWidget(m_progressBar);
    }

    {
        m_labelFileName = new QLabel("", this);
        layout->addWidget(m_labelFileName);
    }

    setLayout(layout);
}

void WizardPackageInstallerStatusPage::initializePage()
{
    m_packagePath = field("introduction.packagePath").toString();
    m_labelPackagePath->setText(m_packagePath);
    if (!m_isInit)
    {
        connect(&PackageManager, &CspPackageManager::signalUpdateFileName, this, [this](const QString &name) {
            /** */
            m_labelFileName->setText(name);
        });

        connect(&PackageManager, &CspPackageManager::signalUpdateProgress, this, [this](int value) {
            /** */
            m_progressBar->setValue(value);
        });

        connect(&PackageManager, &CspPackageManager::signalFinish, this, [this](bool succeed) {
            if (succeed)
            {
                m_isFinish = true;
                emit completeChanged();
            }
            else
            {
                /** TODO */
            }
        });
        m_isInit = true;
        PackageManager.installAsync(m_packagePath);
    }
}

bool WizardPackageInstallerStatusPage::isComplete() const
{
    return (m_progressBar->value() == m_progressBar->maximum()) && m_isFinish;
}

int WizardPackageInstallerStatusPage::nextId() const
{
    return WizardPackageInstaller::Page_Result;
}

WizardPackageInstallerResultPage::WizardPackageInstallerResultPage(QWidget *parent)
    : QWizardPage(parent),
      m_labelResult(nullptr)
{
    setTitle(tr("Install Result"));
    setSubTitle(tr("Installation completed"));
    setFinalPage(true);

    QVBoxLayout *layout = new QVBoxLayout(this);
    layout->setSpacing(16);

    {
        m_labelResult = new QLabel(tr("The package has been successfully installed"), this);
        m_labelResult->setWordWrap(true);
        layout->addWidget(m_labelResult);
    }

    setLayout(layout);
}

void WizardPackageInstallerResultPage::initializePage()
{
}
