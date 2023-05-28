/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        chip_summary_table.h
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

#ifndef COMMON_REPO_CHIP_SUMMARY_TABLE_H
#define COMMON_REPO_CHIP_SUMMARY_TABLE_H

#include "qtyaml.h"

namespace csp {
class chip_summary_table {
public:
    typedef struct
    {
        QMap<QString, QString> url;
    } document_t;

    typedef struct
    {
        QMap<QString, QString> description;
    } module_t;

    typedef QMap<QString, QMap<QString, document_t>> documents_t;
    typedef QMap<QString, QMap<QString, module_t>>   modules_t;

    typedef struct
    {
        QString                clocktree;
        QString                company;
        QMap<QString, QString> company_url;
        documents_t            documents;
        QString                hal;
        bool                   has_powerpad;
        QMap<QString, QString> illustrate;
        QMap<QString, QString> introduction;
        QString                line;
        modules_t              modules;
        QString                name;
        QString                package;
        QString                series;
        QMap<QString, QString> url;
    } chip_summary_t;

public:
    static chip_summary_t load_chip_summary(const QString &path);
    static chip_summary_t load_chip_summary(const QString &company, const QString &name);

private:
    explicit chip_summary_table();
    ~chip_summary_table();
};
}  // namespace csp

namespace YAML {

template <> struct convert<csp::chip_summary_table::document_t>
{
    static Node encode(const csp::chip_summary_table::document_t &rhs)
    {
        Node node;
        node.force_insert("Url", rhs.url);
        return node;
    }

    static bool decode(const Node &node, csp::chip_summary_table::document_t &rhs)
    {
        if (!node.IsMap() || node.size() != 1)
            return false;

        rhs.url = node["Url"].as<QMap<QString, QString>>();
        return true;
    }
};

template <> struct convert<csp::chip_summary_table::module_t>
{
    static Node encode(const csp::chip_summary_table::module_t &rhs)
    {
        Node node;
        node.force_insert("Description", rhs.description);
        return node;
    }

    static bool decode(const Node &node, csp::chip_summary_table::module_t &rhs)
    {
        if (!node.IsMap() || node.size() != 1)
            return false;

        rhs.description = node["Description"].as<QMap<QString, QString>>();
        return true;
    }
};

template <> struct convert<csp::chip_summary_table::chip_summary_t>
{
    static Node encode(const csp::chip_summary_table::chip_summary_t &rhs)
    {
        Node node;
        node.force_insert("ClockTree", rhs.clocktree);
        node.force_insert("Company", rhs.company);
        node.force_insert("CompanyUrl", rhs.company_url);
        node.force_insert("Documents", rhs.documents);
        node.force_insert("HAL", rhs.hal);
        node.force_insert("HasPowerPad", rhs.has_powerpad);
        node.force_insert("Illustrate", rhs.illustrate);
        node.force_insert("Introduction", rhs.introduction);
        node.force_insert("Line", rhs.line);
        node.force_insert("Modules", rhs.modules);
        node.force_insert("Name", rhs.name);
        node.force_insert("Package", rhs.package);
        node.force_insert("Series", rhs.series);
        node.force_insert("Url", rhs.url);
        return node;
    }

    static bool decode(const Node &node, csp::chip_summary_table::chip_summary_t &rhs)
    {
        if (!node.IsMap() || node.size() != 14)
            return false;

        rhs.clocktree    = node["ClockTree"].as<QString>();
        rhs.company      = node["Company"].as<QString>();
        rhs.company_url  = node["CompanyUrl"].as<QMap<QString, QString>>();
        rhs.documents    = node["Documents"].as<csp::chip_summary_table::documents_t>();
        rhs.hal          = node["HAL"].as<QString>();
        rhs.has_powerpad = node["HasPowerPad"].as<bool>();
        rhs.illustrate   = node["Illustrate"].as<QMap<QString, QString>>();
        rhs.introduction = node["Introduction"].as<QMap<QString, QString>>();
        rhs.line         = node["Line"].as<QString>();
        rhs.modules      = node["Modules"].as<csp::chip_summary_table::modules_t>();
        rhs.name         = node["Name"].as<QString>();
        rhs.package      = node["Package"].as<QString>();
        rhs.series       = node["Series"].as<QString>();
        rhs.url          = node["Url"].as<QMap<QString, QString>>();
        return true;
    }
};
}  // namespace YAML
#endif  // COMMON_REPO_CHIP_SUMMARY_TABLE_H
