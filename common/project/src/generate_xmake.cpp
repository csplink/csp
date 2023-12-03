/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        generate_xmake.cpp
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
 *  2023-07-04     xqyjlj       initial version
 */

#include <QDateTime>
#include <QFile>

#include "configure.h"
#include "generate_xmake.h"
#include "os.h"

generate_xmake::generate_xmake() = default;

generate_xmake::~generate_xmake() = default;

void generate_xmake::replace_var(QString &buffer, const QString &key, const QString &value, const bool is_newline)
{
    QString keyword;
    if (is_newline)
    {
        keyword = QString("${{%1}}\n").arg(key);
    }
    else
    {
        keyword = QString("${{%1}}").arg(key);
    }
    buffer.replace(keyword, value);
}

void generate_xmake::replace_var(QString &buffer, const QString &key, const QStringList &values, const bool is_newline)
{
    QString keyword;
    if (is_newline)
    {
        keyword = QString("${{%1}}\n").arg(key);
    }
    else
    {
        keyword = QString("${{%1}}").arg(key);
    }
    buffer.replace(keyword, values.join("\n"));
}

void generate_xmake::add_includes(QString &buffer, const QStringList &values)
{
    QStringList list;
    for (int i = 0; i < values.size(); i++)
    {
        QString str = QString("includes(\"%1\")").arg(values.at(i));
        list.append(str);
    }
    replace_var(buffer, "includes", list);
}

void generate_xmake::add_requires(QString &buffer, const QStringList &values)
{
    QStringList list;
    for (int i = 0; i < values.size(); i++)
    {
        QString str = QString("add_requires(\"%1\")").arg(values.at(i));
        list.append(str);
    }
    replace_var(buffer, "requires", list);
}

void generate_xmake::add_warnings(QString &buffer, const QStringList &values)
{
    QStringList list;
    QStringList warnings;
    for (int i = 0; i < values.size(); i++)
    {
        QString str = QString("\"%1\"").arg(values.at(i));
        warnings.append(str);
    }
    if (!values.isEmpty())
    {
        list.append("");
        if (values.contains("allextra"))
        {
            list.append("    -- allextra: Enable all warnings + extra warnings (-Wall -Wextra)");
        }
        if (values.contains("error"))
        {
            list.append("    -- error: Use all warnings as compilation errors (-Werror)");
        }
        list.append(QString("    add_requires(%1)").arg(warnings.join(", ")));
        list.append("");
    }

    replace_var(buffer, "warnings", list.join("\n"));
}

void generate_xmake::add_languages(QString &buffer, const QStringList &values)
{
    QStringList list;
    for (int i = 0; i < values.size(); i++)
    {
        QString str = QString("\"%1\"").arg(values.at(i));
        list.append(str);
    }
    replace_var(buffer, "languages", list.join(", "));
}

void generate_xmake::add_deps(QString &buffer, const QStringList &values)
{
    QStringList list;
    for (int i = 0; i < values.size(); i++)
    {
        QString str = QString("    add_deps(\"%1\")").arg(values.at(i));
        list.append(str);
    }
    if (!values.isEmpty())
    {
        list.insert(0, "");
        list.append("");
    }
    replace_var(buffer, "deps", list, true);
}

void generate_xmake::add_rules(QString &buffer, const QStringList &values)
{
    QStringList list;
    for (int i = 0; i < values.size(); i++)
    {
        QString str = QString("    add_rules(\"%1\")").arg(values.at(i));
        list.append(str);
    }
    if (!values.isEmpty())
    {
        list.insert(0, "");
        list.append("");
    }
    replace_var(buffer, "rules", list, true);
}

void generate_xmake::add_includedirs(QString &buffer, const QStringList &values)
{
    QStringList list;
    for (int i = 0; i < values.size(); i++)
    {
        QString str = QString("    add_includedirs(\"%1\")").arg(values.at(i));
        list.append(str);
    }
    if (!values.isEmpty())
    {
        list.insert(0, "");
        list.append("");
    }
    replace_var(buffer, "includedirs", list, true);
}

void generate_xmake::add_files(QString &buffer, const QStringList &values)
{
    QStringList list;
    for (int i = 0; i < values.size(); i++)
    {
        QString str = QString("    add_files(\"%1\")").arg(values.at(i));
        list.append(str);
    }
    if (!values.isEmpty())
    {
        list.insert(0, "");
        list.append("");
    }
    replace_var(buffer, "files", list, true);
}

QString generate_xmake::generate(const project_table::project_t &project_table)
{
    const QDateTime date_time = QDateTime::currentDateTime();
    const QString date = date_time.toString("yyyy-MM-dd hh:mm:ss");
    const QString version = CONFIGURE_PROJECT_VERSION;
    const QString project_name = project_table.core.name;
    const QString hal = project_table.core.hal;
    const QString toolchains = project_table.core.toolchains;
    const QString linkscript = "../../libraries/cmsis/Source/gcc/gcc_APM32F10xxE.ld";
    const QStringList warnings = {"allextra", "error"};
    const QStringList languages = {"c99"};
    const QStringList rules = {"csp.bin", "csp.map", "csp.cpu"};

    QString buffer = os::readfile(":/lib/project/template/xmake.lua");

    replace_var(buffer, "version", version);
    replace_var(buffer, "date", date);
    replace_var(buffer, "project", project_name);
    replace_var(buffer, "hal", hal);
    replace_var(buffer, "toolchains", toolchains);
    replace_var(buffer, "linkscript", linkscript);

    add_includes(buffer, {});
    add_requires(buffer, {});
    add_warnings(buffer, warnings);
    add_languages(buffer, languages);
    add_deps(buffer, {});
    add_rules(buffer, rules);
    add_includedirs(buffer, {});
    add_files(buffer, {});

    return buffer;
}
