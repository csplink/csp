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
#include <QDebug>
#include <QFile>
#include <QFileDialog>
#include <QVBoxLayout>

#include "Configure.h"
#include "Settings.h"
#include "WizardPackageInstaller.h"
#include "quazip.h"
#include "quazipfile.h"

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
    setOption(HaveHelpButton, true);

    setPage(0, new WizardPackageInstallerIntroPage(this, path));
    setPage(1, new WizardPackageInstallerStatusPage(this));

    setStartId(1);
}

void WizardPackageInstaller::accept()
{
    QDialog::accept();
}

WizardPackageInstallerIntroPage::WizardPackageInstallerIntroPage(QWidget *parent, const QString &path)
    : QWizardPage(parent),
      m_lineEditPackagePath(nullptr),
      m_pushButtonChoosePackagePath(nullptr)
{
    setTitle(tr("Version %1").arg(CONFIGURE_PROJECT_VERSION));
    setSubTitle(tr("This wizard will help install a package"));

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

    if (!path.isEmpty() && QFile::exists(path) && path.endsWith(".csppkg"))
    {
        m_lineEditPackagePath->setText(path);
        m_pushButtonChoosePackagePath->setEnabled(false);
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

int WizardPackageInstallerIntroPage::nextId() const
{
    return 1;
}

WizardPackageInstallerStatusPage::WizardPackageInstallerStatusPage(QWidget *parent)
    : QWizardPage(parent),
      m_packagePath(),
      m_labelPackagePath(nullptr)
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

    setLayout(layout);
}

void WizardPackageInstallerStatusPage::initializePage()
{
    m_packagePath = field("introduction.packagePath").toString();
    m_labelPackagePath->setText(m_packagePath);
}

int WizardPackageInstallerStatusPage::nextId() const
{
    return 2;
}

void WizardPackageInstallerStatusPage::installPackage()
{
    QuaZip archive(m_packagePath);
    if (archive.open(QuaZip::mdUnzip))
    {
        QString dstPath = Settings.repository();
        QDir dir(dstPath);
        //        int count = archive.getEntriesCount();
        //        int i = 0;
        QString fileName;

        for (bool f = archive.goToFirstFile(); f; f = archive.goToNextFile())
        {
            fileName = archive.getCurrentFileName();
            if (fileName.endsWith("/"))
            {
                dir.mkpath(fileName);
            }
            else
            {
                QuaZipFile zipFile;
                QByteArray data;
                QFile dstFile;

                zipFile.setZipName(archive.getZipName());
                zipFile.setFileName(fileName);
                zipFile.open(QIODevice::ReadOnly);
                data = zipFile.readAll();
                zipFile.close();

                dstFile.setFileName(dstPath + fileName);
                if (!dstFile.open(QIODevice::WriteOnly))
                {
                    return;
                }
                dstFile.write(data);
                QCoreApplication::processEvents(QEventLoop::AllEvents, 100);
                dstFile.close();
                //                i++;
                // 这里可以获得解压进度，一般来说解压操作是放在多线程的，所以使用信号发送
                // void sigUnzipping(int current, int total)
                // emit sigUnzipping(i, count);
            }
        }
    }
    else
    {
    }
}
