/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        repository_table.h
 *  @brief
 *
 * ****************************************************************************
 *  @attention
 *  Licensed under the GNU Lesser General Public License v. 3 (the "License");
 *  You may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      https://www.gnu.org/licenses/lgpl-3.0.html
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

#ifndef COMMON_REPO_REPOSITORY_TABLE_H
#define COMMON_REPO_REPOSITORY_TABLE_H

#include "qtyaml.h"

namespace csp {
class repository_table {
public:
    typedef struct
    {
        float lowest;
        float run;
    } current_t;

    typedef struct
    {
        float max;
        float min;
    } temperature_t;

    typedef struct
    {
        float max;
        float min;
    } voltage_t;

    typedef struct
    {
        QString            core;
        current_t          current;
        float              flash;
        float              frequency;
        int                io;
        QString            package;
        QMap<QString, int> peripherals;
        float              price;
        float              ram;
        temperature_t      temperature;
        voltage_t          voltage;
    } chip_info_t;

    typedef QMap<QString, chip_info_t> chip_line_t;

    typedef QMap<QString, chip_line_t> chip_series_t;

    typedef QMap<QString, chip_series_t> chip_company_t;

    typedef QMap<QString, chip_company_t> chip_t;

    typedef struct
    {
        chip_t chips;
    } repository_t;

public:
    static repository_t get_repository(const QString &path);

private:
    explicit repository_table();
    ~repository_table();
};
}  // namespace csp

namespace YAML {

template <> struct convert<csp::repository_table::current_t>
{
    static Node encode(const csp::repository_table::current_t &rhs)
    {
        Node node;
        node.force_insert("Lowest", rhs.lowest);
        node.force_insert("Run", rhs.run);
        return node;
    }

    static bool decode(const Node &node, csp::repository_table::current_t &rhs)
    {
        if (!node.IsMap() || node.size() != 2)
            return false;

        rhs.lowest = node["Lowest"].as<float>();
        rhs.run    = node["Run"].as<float>();
        return true;
    }
};

template <> struct convert<csp::repository_table::temperature_t>
{
    static Node encode(const csp::repository_table::temperature_t &rhs)
    {
        Node node;
        node.force_insert("Max", rhs.max);
        node.force_insert("Min", rhs.min);
        return node;
    }

    static bool decode(const Node &node, csp::repository_table::temperature_t &rhs)
    {
        if (!node.IsMap() || node.size() != 2)
            return false;

        rhs.max = node["Max"].as<float>();
        rhs.min = node["Min"].as<float>();
        return true;
    }
};

template <> struct convert<csp::repository_table::voltage_t>
{
    static Node encode(const csp::repository_table::voltage_t &rhs)
    {
        Node node;
        node.force_insert("Max", rhs.max);
        node.force_insert("Min", rhs.min);
        return node;
    }

    static bool decode(const Node &node, csp::repository_table::voltage_t &rhs)
    {
        if (!node.IsMap() || node.size() != 2)
            return false;

        rhs.max = node["Max"].as<float>();
        rhs.min = node["Min"].as<float>();
        return true;
    }
};

template <> struct convert<csp::repository_table::chip_info_t>
{
    static Node encode(const csp::repository_table::chip_info_t &rhs)
    {
        Node node;
        node.force_insert("Core", rhs.core);
        node.force_insert("Current", rhs.current);
        node.force_insert("Flash", rhs.flash);
        node.force_insert("Frequency", rhs.frequency);
        node.force_insert("IO", rhs.io);
        node.force_insert("Package", rhs.package);
        node.force_insert("Peripherals", rhs.peripherals);
        node.force_insert("Ram", rhs.ram);
        node.force_insert("Temperature", rhs.temperature);
        node.force_insert("Voltage", rhs.voltage);
        return node;
    }

    static bool decode(const Node &node, csp::repository_table::chip_info_t &rhs)
    {
        if (!node.IsMap() || node.size() != 10)
            return false;

        rhs.core        = node["Core"].as<QString>();
        rhs.current     = node["Current"].as<csp::repository_table::current_t>();
        rhs.flash       = node["Flash"].as<float>();
        rhs.frequency   = node["Frequency"].as<float>();
        rhs.io          = node["IO"].as<int>();
        rhs.package     = node["Package"].as<QString>();
        rhs.peripherals = node["Peripherals"].as<QMap<QString, int>>();
        rhs.ram         = node["Ram"].as<float>();
        rhs.temperature = node["Temperature"].as<csp::repository_table::temperature_t>();
        rhs.voltage     = node["Voltage"].as<csp::repository_table::voltage_t>();
        return true;
    }
};

template <> struct convert<csp::repository_table::repository_t>
{
    static Node encode(const csp::repository_table::repository_t &rhs)
    {
        Node node;
        node.force_insert("Chips", rhs.chips);
        return node;
    }

    static bool decode(const Node &node, csp::repository_table::repository_t &rhs)
    {
        if (!node.IsMap() || node.size() != 1)
            return false;

        rhs.chips = node["Chips"].as<csp::repository_table::chip_t>();
        return true;
    }
};
}  // namespace YAML

#endif  // COMMON_REPO_REPOSITORY_TABLE_H
