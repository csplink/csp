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
#include <QProcess>
#include <QRegularExpression>

#include "config.h"
#include "os.h"
#include "path.h"
#include "qtjson.h"
#include "xmake.h"

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(xmake::version_t, size, installed, sha256)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(xmake::info_t, versions, urls, homepage, description, license, company)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(xmake::packages_t, toolchain, library)
} // namespace nlohmann

QT_DEBUG_ADD_TYPE(xmake::version_t)
QT_DEBUG_ADD_TYPE(xmake::info_t)
QT_DEBUG_ADD_TYPE(xmake::packages_t)

xmake::xmake()
{
    _process = new QProcess();
}

xmake::~xmake()
{
    delete _process;
    _process = nullptr;
}

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

    if (!program.isEmpty())
    {
        if (os::execv(program, { "--version" }, config::env(), 10000, config::default_workdir(), &output, nullptr))
        {
            static const QRegularExpression regex(R"(v(\d+\.\d+\.\d+\+\w+\.\w+))");
            const QRegularExpressionMatch match = regex.match(output);

            if (match.hasMatch())
            {
                version = "v" + match.captured(1);
            }
        }
    }
    else
    {
        return "";
    }
    return version;
}

QString xmake::lua(const QString &lua_path, const QStringList &args)
{
    QString output;
    if (!lua_path.isEmpty())
    {
        QStringList list = { "-D", path::absolute(lua_path) };
        list << args;
        output = cmd("lua", list);
    }
    else
    {
        output = "";
        // TODO: Invalid parameter
    }
    return output;
}

QString xmake::cmd(const QString &command, const QStringList &args, const QString &program, const QString &workdir)
{
    QByteArray output;
    if (!command.isEmpty() && !program.isEmpty() && !workdir.isEmpty())
    {
        QStringList list = { command, "-D" };
        list << args;

        (void)os::execv(program, list, config::env(), 10000, workdir, &output, nullptr);
    }
    else
    {
        output = "";
        // TODO: Invalid parameter
    }

    return output;
}

void xmake::cmd_log(const QString &command, const QStringList &args, const QString &program, const QString &workdir)
{
    const QMap<QString, QString> env = config::env();
    QStringList list;
    if (!command.isEmpty())
    {
        list = QStringList{ command, "-D" };
    }
    list << args;

    QProcessEnvironment environment = QProcessEnvironment::systemEnvironment();
    auto env_i = env.constBegin();
    while (env_i != env.constEnd())
    {
        environment.insert(env_i.key(), env_i.value());
        ++env_i;
    }

    _process->setProgram(program);
    _process->setArguments(list);
    _process->setProcessEnvironment(environment);

    if (os::isdir(workdir))
    {
        _process->setWorkingDirectory(workdir);
    }

    log(QString("%1 %2").arg(program, list.join(" ")));
    _process->start();

    (void)connect(_process, &QProcess::readyReadStandardOutput, this, &xmake::ready_read_standard_output_callback,
                  Qt::UniqueConnection);

    if (!_process->waitForFinished(30000))
    {
        log("failed;");
    }
    else
    {
        log("");
    }
}

void xmake::load_packages(packages_t *packages, const QString &repositories)
{
    if (packages != nullptr && !repositories.isEmpty())
    {
        const QString data = xmake::cmd("csp-repo", { "--dump=json", QString("--repositories=") + repositories });
        try
        {
            const std::string buffer = data.toStdString();
            const nlohmann::json json = nlohmann::json::parse(buffer);
            (void)json.get_to(*packages);
        }
        catch (std::exception &e)
        {
            const QString str = QString("try to parse packages failed. \n\nreason: %1").arg(e.what());
            qWarning().noquote() << str;
            packages->library.clear();
            packages->toolchain.clear();
        }
    }
    else
    {
        // TODO: Invalid parameter
    }
}

void xmake::install_package(const QString &name, const QString &version, const QString &repositories)
{
    if (!name.isEmpty() && !version.isEmpty() && !repositories.isEmpty())
    {
        cmd_log("csp-repo", { QString("--install=%1@%2").arg(name, version), QString("--repositories=") + repositories });
    }
}

void xmake::update_package(const QString &name, const QString &repositories)
{
    if (!name.isEmpty() && !repositories.isEmpty())
    {
        cmd_log("csp-repo", { QString("--update=") + name, QString("--repositories=") + repositories });
    }
}

void xmake::uninstall_package(const QString &name, const QString &version, const QString &repositories)
{
    if (!name.isEmpty() && !version.isEmpty() && !repositories.isEmpty())
    {
        cmd_log("csp-repo", { QString("--uninstall=%1@%2").arg(name, version), QString("--repositories=") + repositories });
    }
}

void xmake::install_log_handler(const log_handler handler)
{
    _log_handler = handler;
}

void xmake::csp_repo_dump_log(const QString &type)
{
    if (!type.isEmpty())
    {
        cmd_log("csp-repo", { QString("--dump=") + type });
    }
    else
    {
        // TODO: Invalid parameter
    }
}

void xmake::csp_coder_log(const QString &project_file, const QString &output, const QString &repositories)
{
    if (!project_file.isEmpty() && !output.isEmpty() && !repositories.isEmpty())
    {
        cmd_log("csp-coder", { QString("--project-file=") + project_file, QString("--output=") + output,
                               QString("--repositories=") + repositories });
    }
    else
    {
        // TODO: Invalid parameter
    }
}

void xmake::build_log(const QString &projectdir, const QString &mode)
{
    if (!projectdir.isEmpty() && !mode.isEmpty() && os::isdir(projectdir))
    {
        cmd_log("f", { "-y", "-m", mode }, config::tool_xmake(), projectdir);
        cmd_log("", { "-y", "-j8" }, config::tool_xmake(), projectdir);
    }
    else
    {
        // TODO: Invalid parameter
    }
}

void xmake::ready_read_standard_output_callback() const
{
    const QByteArray err = _process->readAllStandardOutput();
    qDebug() << err;
    if (!err.isEmpty())
    {
        xmake::log(err.trimmed());
    }
}
