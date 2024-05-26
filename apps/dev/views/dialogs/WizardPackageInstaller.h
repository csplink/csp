/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        WizardPackageInstaller.h
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
 */

#ifndef WIZARD_PACKAGE_INSTALLER_H
#define WIZARD_PACKAGE_INSTALLER_H

#include <QLabel>
#include <QLineEdit>
#include <QProgressBar>
#include <QPushButton>
#include <QWizard>
#include <QWizardPage>

class WizardPackageInstaller final : public QWizard
{
    Q_OBJECT
  public:
    explicit WizardPackageInstaller(QWidget *parent, const QString &path = "");
    void accept() override;
};

class WizardPackageInstallerIntroPage : public QWizardPage
{
    Q_OBJECT
  public:
    WizardPackageInstallerIntroPage(QWidget *parent, const QString &path);
    int nextId() const override;

  private:
    QLineEdit *m_lineEditPackagePath;
    QPushButton *m_pushButtonChoosePackagePath;
};

class WizardPackageInstallerStatusPage : public QWizardPage
{
    Q_OBJECT
  public:
    WizardPackageInstallerStatusPage(QWidget *parent);
    void initializePage() override;
    int nextId() const override;

  private:
    QString m_packagePath;
    QLabel *m_labelPackagePath;
    QProgressBar *m_progressBar;

    void installPackage();
};

#endif /** WIZARD_PACKAGE_INSTALLER_H */
