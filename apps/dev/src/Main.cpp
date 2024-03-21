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
 *  2023-04-18     xqyjlj       initial version
 */

#include <QApplication>
#include <QCommandLineParser>
#include <QDebug>
#include <QDir>
#include <QFile>
#include <QFontDatabase>
#include <QTranslator>

#include "Config.h"
#include "Configure.h"
#include "Project.h"
#include "Repo.h"
#include "ViewMainWindow.h"

static void init()
{
    Q_INIT_RESOURCE(project);
    Q_INIT_RESOURCE(qtpropertybrowser);
    Q_INIT_RESOURCE(repo);

    Config::init();
    repo::init();
    Project::init();
}

static void deinit()
{
    Project::deinit();
    repo::deinit();
    Config::deinit();

    Q_CLEANUP_RESOURCE(repo);
    Q_CLEANUP_RESOURCE(qtpropertybrowser);
    Q_CLEANUP_RESOURCE(project);
}

int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);

    QApplication app(argc, argv);
    QApplication::setApplicationName("csp-dev");
    QApplication::setApplicationVersion(CONFIGURE_PROJECT_VERSION);
    QApplication::setOrganizationName("csplink");
    QApplication::setOrganizationName("csplink.top");

    init();

    const QDir fontsDir("./fonts");
    for (const QFileInfo &dir : fontsDir.entryInfoList({ "*" }, QDir::Dirs | QDir::NoDotAndDotDot | QDir::NoSymLinks))
    {
        const QDir fontDir(dir.absoluteFilePath());

        for (const QFileInfo &file : fontDir.entryInfoList({ "*.ttf" }, QDir::Files | QDir::Hidden | QDir::NoSymLinks))
        {
            const auto id = QFontDatabase::addApplicationFont(file.absoluteFilePath());
            if (id == -1)
            {
                qDebug() << QObject::tr("load font: <%1> failed.").arg(file.absoluteFilePath());
            }
        }
    }

    const QDir qmDir("./translations");
    for (const QFileInfo &file : qmDir.entryInfoList({ QString("*%1.qm").arg(Config::language()) }, QDir::Files | QDir::Hidden | QDir::NoSymLinks))
    {
        const auto translator = new QTranslator(&app);
        translator->load(file.absoluteFilePath());
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
        const auto file = parser.positionalArguments().at(0);
        if (!QFile::exists(file))
        {
            qCritical().noquote() << QObject::tr("file: <%1> is not exist.").arg(file);
        }
        else
        {
            try
            {
                Project::getInstance()->loadProject(file);
            }
            catch (const std::exception &e)
            {
                qCritical().noquote() << e.what();
                return EINVAL;
            }
        }
    }

    QApplication::setWindowIcon(QIcon(":/images/logo.ico"));
    ViewMainWindow w;
    w.show();

    const int rtn = QApplication::exec();

    deinit();

    return rtn;
}
