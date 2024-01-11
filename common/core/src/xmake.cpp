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

void xmake::init()
{
    if (_instance == nullptr)
    {
        _instance = new xmake();
    }
}

void xmake::deinit()
{
    delete _instance;
    _instance = nullptr;
}

xmake *xmake::get_instance()
{
    return _instance;
}

QString xmake::version(const QString &program)
{
    QByteArray output;
    QString version;

    Q_ASSERT(!program.isEmpty());

    if (os::execv(program, {"--version"}, config::env(), 10000, config::default_workdir(), &output, nullptr))
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

QString xmake::lua(const QString &lua_path, const QStringList &args)
{
    Q_ASSERT(!lua_path.isEmpty());

    QStringList list = {"-D", path::absolute(lua_path)};
    list << args;

    QString output = cmd("lua", list);

    return output;
}

QString xmake::cmd(const QString &command, const QStringList &args, const QString &program, const QString &workdir)
{
    QByteArray output;
    Q_ASSERT(!command.isEmpty());
    Q_ASSERT(!program.isEmpty());
    Q_ASSERT(!workdir.isEmpty());

    QStringList list = {command, "-D"};
    list << args;

    os::execv(program, list, config::env(), 10000, workdir, &output, nullptr);

    return output;
}

void xmake::load_packages(packages_t *packages)
{
    const QString repodir = config::repodir();

    Q_ASSERT(packages != nullptr);

    const QString yml = xmake::cmd("csp-repo", {"--dump=json"});
    try
    {
        const std::string buffer = yml.toStdString();
        const nlohmann::json json = nlohmann::json::parse(buffer);
        json.get_to(*packages);
    }
    catch (std::exception &e)
    {
        const QString str = QString("try to parse packages failed. \n\nreason: %1").arg(e.what());
        qWarning().noquote() << str;
        packages->library.clear();
        packages->toolchain.clear();
    }
}

void xmake::install_log_handler(const log_handler handler)
{
    _log_handler = handler;
}
