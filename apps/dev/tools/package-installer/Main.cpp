/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        Main.cpp
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
 *  2024-05-20     xqyjlj       initial version
 */

#include <QApplication>
#include <QCommandLineParser>
#include <QDebug>
#include <QDir>
#include <QFile>
#include <QFontDatabase>
#include <QIcon>
#include <QTranslator>

#include "Configure.h"
#include "Settings.h"
#include "WizardPackageInstaller.h"

int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);

    QApplication app(argc, argv);
    QApplication::setApplicationName("csp-package-installer");
    QApplication::setApplicationVersion(CONFIGURE_PROJECT_VERSION);
    QApplication::setOrganizationName("csplink");
    QApplication::setOrganizationName("csplink.top");

    const QDir fontsDir("./fonts");
    const QFileInfoList fontsDirList =
        fontsDir.entryInfoList({"*"}, QDir::Dirs | QDir::NoDotAndDotDot | QDir::NoSymLinks);
    for (const QFileInfo &dir : fontsDirList)
    {
        const QDir fontDir(dir.absoluteFilePath());
        const QFileInfoList fontDirList =
            fontDir.entryInfoList({"*.ttf"}, QDir::Files | QDir::Hidden | QDir::NoSymLinks);
        for (const QFileInfo &file : fontDirList)
        {
            const auto id = QFontDatabase::addApplicationFont(file.absoluteFilePath());
            if (id == -1)
            {
                qDebug() << QObject::tr("load font: <%1> failed.").arg(file.absoluteFilePath());
            }
        }
    }

    const QDir qmDir("./translations");
    const QFileInfoList qmDirList = qmDir.entryInfoList({QString("*%1.qm").arg(Settings.language())},
                                                        QDir::Files | QDir::Hidden | QDir::NoSymLinks);
    for (const QFileInfo &file : qmDirList)
    {
        const auto translator = new QTranslator(&app);
        translator->load(file.absoluteFilePath());
        qApp->installTranslator(translator);
    }

    QApplication::setWindowIcon(QIcon(":/images/logo.ico"));

    WizardPackageInstaller wizard(nullptr, "C:/Users/xqyjlj/Downloads/新建文件夹/新建文本文档.csppkg");
    (void)wizard.show();

    const int rtn = QApplication::exec();

    return rtn;
}
