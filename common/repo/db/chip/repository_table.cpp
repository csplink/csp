/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        repository_table.cpp
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
 *  2023-04-20     xqyjlj       initial version
 */

#include <QFile>
#include <QDebug>

#include "db/chip/repository_table.h"
#include "utils.h"

repository_table::repository_table(const QString &path) {
    Q_ASSERT(!path.isEmpty());
    Q_ASSERT(QFile::exists(path));

    try {
        std::string buffer;
        QFile file(path);

        file.open(QFileDevice::ReadOnly | QIODevice::Text);
        buffer = file.readAll().toStdString();
        file.close();
        YAML::Node yaml_data = YAML::Load(buffer);
        this->m_repository = yaml_data.as<repository_table::repository_t>();
    }
    catch (YAML::BadFile &e) {
        utils::show_error_and_exit(e.what());
    }
    catch (YAML::BadConversion &e) {
        utils::show_error_and_exit(e.what());
    }
    catch (std::exception &e) {
        qDebug() << e.what();
        throw;
    }
}

repository_table::repository_t repository_table::get_repository() const {
    return this->m_repository;
}

repository_table::~repository_table() = default;
