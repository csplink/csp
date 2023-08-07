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
#include <QCommandLineParser>
#include <QDebug>
#include <QFontDatabase>
#include <QTranslator>

#include "config.h"
#include "configure.h"
#include "mainwindow_view.h"
#include "os.h"
#include "project.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    QApplication::setApplicationName("csp-dev");
    QApplication::setApplicationVersion(CONFIGURE_PROJECT_VERSION);
    QApplication::setOrganizationName("csplink");
    QApplication::setOrganizationName("csplink.top");

    Q_INIT_RESOURCE(core);
    Q_INIT_RESOURCE(project);
    Q_INIT_RESOURCE(qtpropertybrowser);

    config::init();

    for (const QString &dir : os::dirs("./fonts", QString("*")))
    {
        for (const QString &file : os::files(dir, QString("*.ttf")))
        {
            auto id = QFontDatabase::addApplicationFont(file);
            if (id == -1)
                qDebug() << QObject::tr("load font: <%1> failed.").arg(file);
        }
    }

    for (const QString &file : os::files("./translations", QString("*%1.qm").arg(config::language())))
    {
        auto translator = new QTranslator(&app);
        translator->load(file);
        qApp->installTranslator(translator);
    }

    QCommandLineParser parser;
    parser.setApplicationDescription(QObject::tr("Tools for flexible configuration of chips and boards."));
    parser.addHelpOption();
    parser.addVersionOption();
    parser.addPositionalArgument("file", QObject::tr("Project file path."));

    parser.process(app);

    if (!parser.positionalArguments().isEmpty())
    {
        auto file = parser.positionalArguments().at(0);
        if (!os::isfile(file))
        {
            qCritical() << QObject::tr("file: <%1> is not exist.").arg(file);
            return ENOENT;
        }
        else
        {
            try
            {
                project::get_instance()->load_project(file);
            }
            catch (const std::exception &e)
            {
                qCritical() << e.what();
                return EINVAL;
            }
        }
    }

    app.setWindowIcon(QIcon(":/images/logo.ico"));
    mainwindow_view w;
    w.show();
    return app.exec();
}
