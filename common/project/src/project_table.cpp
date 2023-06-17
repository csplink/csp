/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        project_table.cpp
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
 *  2023-05-27     xqyjlj       initial version
 */

#include <QDebug>
#include <QFile>

#include "os.h"
#include "project_table.h"

namespace csp {

project_table::project_table() = default;

project_table::~project_table() = default;

project_table::project_t project_table::load_project(const QString &path)
{
    Q_ASSERT(!path.isEmpty());
    Q_ASSERT(os::isfile(path));

    try
    {
        std::string buffer;
        QFile       file(path);

        file.open(QFileDevice::ReadOnly | QIODevice::Text);
        buffer = file.readAll().toStdString();
        file.close();
        YAML::Node yaml_data = YAML::Load(buffer);
        return yaml_data.as<project_table::project_t>();
    }
    catch (YAML::BadFile &e)
    {
        os::show_error_and_exit(e.what());
        throw;
    }
    catch (YAML::BadConversion &e)
    {
        os::show_error_and_exit(e.what());
        throw;
    }
    catch (std::exception &e)
    {
        qDebug() << e.what();
        throw;
    }

    return {};
}

void project_table::save_project(const project_table::project_t &p, const QString &path)
{
    Q_ASSERT(!path.isEmpty());

    auto  yaml = dump_project(p);
    QFile file(path);
    file.open(QFileDevice::WriteOnly | QIODevice::Text);
    file.write(yaml.toUtf8());
    file.close();
}

QString project_table::dump_project(const project_table::project_t &p)
{
    YAML::Node node;
    node = p;
    return QString::fromStdString(YAML::Dump(node));
}

}  // namespace csp
