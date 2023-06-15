/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        main.cpp
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
 *  2023-04-18     xqyjlj       initial version
 */

#include <QApplication>
#include <QDebug>
#include <QFontDatabase>
#include <QTranslator>

#include "config.h"
#include "mainwindow_view.h"
#include "os.h"

using namespace csp;

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    Q_INIT_RESOURCE(qtpropertybrowser);

    for (const QString &dir : os::dirs("./fonts", QString("*")))
    {
        for (const QString &file : os::files(dir, QString("*.ttf")))
        {
            auto id = QFontDatabase::addApplicationFont(file);
            if (id == -1)
                qDebug() << "add font" << file << "failed";
        }
    }

    for (const QString &file : os::files("./translations", QString("*%1.qm").arg(config::language())))
    {
        auto translator = new QTranslator(&a);
        translator->load(file);
        qApp->installTranslator(translator);
    }

    a.setWindowIcon(QIcon(":/images/logo.ico"));
    mainwindow_view w;
    w.show();
    return a.exec();
}
