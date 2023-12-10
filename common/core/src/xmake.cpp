/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        xmake.cpp
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
 *  2023-08-14     xqyjlj       initial version
 */

#include <QDebug>
#include <QFile>
#include <QRegularExpression>

#include "config.h"
#include "os.h"
#include "path.h"
#include "qtjson.h"
#include "xmake.h"

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(xmake::info_t, versions, urls, homepage, description, license)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(xmake::packages_t, toolchain, library)
} // namespace nlohmann

QT_DEBUG_ADD_TYPE(xmake::info_t)
QT_DEBUG_ADD_TYPE(xmake::packages_t)

QString xmake::version(const QString &program)
{
    QByteArray output;
    QString version;

    Q_ASSERT(!program.isEmpty());

    if (os::execv(program, QStringList() << "--version", {}, 10000, "", &output, nullptr))
    {
        const QRegularExpression regex(R"(v(\d+\.\d+\.\d+\+\w+\.\w+))");
        const QRegularExpressionMatch match = regex.match(output);

        if (match.hasMatch())
        {
            version = "v" + match.captured(1);
        }
    }
    return version;
}

QString xmake::lua(const QString &lua_path, const QStringList &args, const QString &program, const QString &workdir)
{
    QByteArray output;

    Q_ASSERT(!lua_path.isEmpty());
    Q_ASSERT(!program.isEmpty());

    if (os::execv(program, QStringList() << "lua" << path::absolute(lua_path) << args, {}, 10000, workdir, &output,
                  nullptr))
    {
    }
    else
    {
        qDebug()
            << QString("%1 lua %2 %3 failed. < %4 >").arg(program, path::absolute(lua_path), args.join(" "), output);
    }

    return output;
}

void xmake::load_packages_byfile(packages_t *packages, const QString &file)
{
    Q_ASSERT(packages != nullptr);
    Q_ASSERT(!file.isEmpty());
    Q_ASSERT(os::isfile(file));

    try
    {
        const std::string buffer = os::readfile(file).toStdString();
        const nlohmann::json json = nlohmann::json::parse(buffer);
        json.get_to(*packages);
    }
    catch (std::exception &e)
    {
        const QString str = QString("try to parse file \"%1\" failed. \n\nreason: %2").arg(file, e.what());
        qCritical() << str;
        os::show_error_and_exit(str);
        throw;
    }
}

void xmake::load_packages(packages_t *packages, const QString &program, const QString &workdir)
{
    const QString repodir = config::repodir();
    const QString script_path = QString("%1/tools/csp/dump_package.lua").arg(repodir);

    Q_ASSERT(packages != nullptr);
    Q_ASSERT(!script_path.isEmpty());
    Q_ASSERT(os::isfile(script_path));
    Q_ASSERT(!program.isEmpty());

    const QString yml = xmake::lua(script_path, {"--json"}, program, workdir);
    try
    {
        const std::string buffer = yml.toStdString();
        const nlohmann::json json = nlohmann::json::parse(buffer);
        json.get_to(*packages);
    }
    catch (std::exception &e)
    {
        const QString str =
            QString("try to parse packages \" xmake l %1\" failed. \n\nreason: %2").arg(script_path, e.what());
        qCritical() << str;
        os::show_error_and_exit(str);
        throw;
    }
}
