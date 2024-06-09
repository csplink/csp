/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        PackageDescriptionTable.cpp
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
 *  Copyright (C) 2023-2024 xqyjlj<xqyjlj@126.com>
 *
 * ****************************************************************************
 *  Change Logs:
 *  Date           Author       Notes
 *  ------------   ----------   -----------------------------------------------
 *  2023-06-04     xqyjlj       initial version
 */

#include <QFile>

#include "Debug.h"
#include "PackageDescriptionTable.h"
#include "QtJson.h"
#include "QtYaml.h"

namespace QT_YAML
{
QT_YAML_GEN_PARSE_CODE(PackageDescriptionTable::AuthorType, Name, Email, Website)
QT_YAML_GEN_PARSE_CODE(PackageDescriptionTable::PackageDescriptionType, Author, Name, Version, License, Type, Vendor,
                       VendorUrl, Description, Url, SupportContact)
} // namespace QT_YAML

namespace QT_JSON
{
QT_JSON_GEN_PARSE_CODE(PackageDescriptionTable::AuthorType, Name, Email, Website)
QT_JSON_GEN_PARSE_CODE(PackageDescriptionTable::PackageDescriptionType, Author, Name, Version, License, Type, Vendor,
                       VendorUrl, Description, Url, SupportContact)
} // namespace QT_JSON

PackageDescriptionTable::PackageDescriptionTable()
    : QObject()
{
}

PackageDescriptionTable::~PackageDescriptionTable()
{
}

bool PackageDescriptionTable::loadPackageDescription(PackageDescriptionType *packageDescription, const QString &path)
{
    bool rtn = false;

    if (packageDescription != nullptr)
    {
        QFile file(path);
        if (file.open(QIODevice::ReadOnly))
        {
            try
            {
                const std::string buffer = file.readAll().toStdString();
                const YAML::Node yaml_data = YAML::Load(buffer);
                YAML::convert<PackageDescriptionType>::decode(yaml_data, *packageDescription);
                rtn = true;
            }
            catch (std::exception &e)
            {
                SHOW_E(nullptr, tr("Package description table"),
                       QString("Try to parse file \"%1\" failed. reason: %2").arg(path, e.what()));
                throw;
            }

            file.close();
        }
        else
        {
            SHOW_W(nullptr, tr("Package description table"), QString("The file %1 not found!").arg(path));
        }
    }
    else
    {
        SHOW_W(nullptr, tr("Package description table"), "The packageDescription ptr is nullptr!");
    }
    return rtn;
}
