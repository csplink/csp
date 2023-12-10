/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        chip_summary_table.cpp
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
 *  2023-05-21     xqyjlj       initial version
 */

#include <QDebug>
#include <QFile>

#include "chip_summary_table.h"
#include "config.h"
#include "os.h"
#include "qtjson.h"
#include "qtyaml.h"

namespace YAML
{
YAML_DEFINE_TYPE_NON_INTRUSIVE(chip_summary_table::document_t, url)
YAML_DEFINE_TYPE_NON_INTRUSIVE(chip_summary_table::module_t, description)
YAML_DEFINE_TYPE_NON_INTRUSIVE(chip_summary_table::chip_summary_t, clocktree, company, company_url, documents, hal,
                               has_powerpad, illustrate, introduction, line, modules, name, package, series, url)
} // namespace YAML

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(chip_summary_table::document_t, url)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(chip_summary_table::module_t, description)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(chip_summary_table::chip_summary_t, clocktree, company, company_url, documents, hal,
                                   has_powerpad, illustrate, introduction, line, modules, name, package, series, url)
} // namespace nlohmann
QT_DEBUG_ADD_TYPE(chip_summary_table::document_t)
QT_DEBUG_ADD_TYPE(chip_summary_table::module_t)
QT_DEBUG_ADD_TYPE(chip_summary_table::chip_summary_t)

chip_summary_table::chip_summary_table() = default;

chip_summary_table::~chip_summary_table() = default;

chip_summary_table::chip_summary_t chip_summary_table::load_chip_summary(const QString &path)
{
    Q_ASSERT(!path.isEmpty());
    Q_ASSERT(os::isfile(path));

    try
    {
        QFile file(path);

        file.open(QFileDevice::ReadOnly | QIODevice::Text);
        const std::string buffer = file.readAll().toStdString();
        file.close();
        const YAML::Node yaml_data = YAML::Load(buffer);
        return yaml_data.as<chip_summary_table::chip_summary_t>();
    }
    catch (std::exception &e)
    {
        const QString str = QString("try to parse file \"%1\" failed. \n\nreason: %2").arg(path, e.what());
        qCritical() << str;
        os::show_error_and_exit(str);
        throw;
    }
}

chip_summary_table::chip_summary_t chip_summary_table::load_chip_summary(const QString &company, const QString &name)
{
    Q_ASSERT(!company.isEmpty());
    Q_ASSERT(!name.isEmpty());

    const QString path = QString("%1/db/chips/%2/%3.yml").arg(config::repodir(), company.toLower(), name.toLower());
    return load_chip_summary(path);
}
