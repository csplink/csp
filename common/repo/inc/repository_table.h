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

#include <QResource>

#include "qtyaml.h"

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
    } mcu_t;

    typedef QMap<QString, mcu_t> line_t;

    typedef QMap<QString, line_t> series_t;

    typedef QMap<QString, series_t> company_t;

    typedef QMap<QString, company_t> repository_t;

private:
    repository_t m_repository;

public:
    explicit repository_table(const QString &path);
    ~repository_table();

    [[nodiscard]] repository_t get_repository() const;
};

namespace YAML {

template <> struct convert<repository_table::current_t>
{
    static Node encode(const repository_table::current_t &rhs)
    {
        Node node;
        node.force_insert("lowest", rhs.lowest);
        node.force_insert("run", rhs.run);
        return node;
    }

    static bool decode(const Node &node, repository_table::current_t &rhs)
    {
        if (!node.IsMap() || node.size() != 2)
            return false;

        rhs.lowest = node["lowest"].as<float>();
        rhs.run    = node["run"].as<float>();
        return true;
    }
};

template <> struct convert<repository_table::temperature_t>
{
    static Node encode(const repository_table::temperature_t &rhs)
    {
        Node node;
        node.force_insert("max", rhs.max);
        node.force_insert("min", rhs.min);
        return node;
    }

    static bool decode(const Node &node, repository_table::temperature_t &rhs)
    {
        if (!node.IsMap() || node.size() != 2)
            return false;

        rhs.max = node["max"].as<float>();
        rhs.min = node["min"].as<float>();
        return true;
    }
};

template <> struct convert<repository_table::voltage_t>
{
    static Node encode(const repository_table::voltage_t &rhs)
    {
        Node node;
        node.force_insert("max", rhs.max);
        node.force_insert("min", rhs.min);
        return node;
    }

    static bool decode(const Node &node, repository_table::voltage_t &rhs)
    {
        if (!node.IsMap() || node.size() != 2)
            return false;

        rhs.max = node["max"].as<float>();
        rhs.min = node["min"].as<float>();
        return true;
    }
};

template <> struct convert<repository_table::mcu_t>
{
    static Node encode(const repository_table::mcu_t &rhs)
    {
        Node node;
        node.force_insert("core", rhs.core);
        node.force_insert("current", rhs.current);
        node.force_insert("flash", rhs.flash);
        node.force_insert("frequency", rhs.frequency);
        node.force_insert("io", rhs.io);
        node.force_insert("package", rhs.package);
        node.force_insert("peripherals", rhs.peripherals);
        node.force_insert("ram", rhs.ram);
        node.force_insert("temperature", rhs.temperature);
        node.force_insert("voltage", rhs.voltage);
        return node;
    }

    static bool decode(const Node &node, repository_table::mcu_t &rhs)
    {
        if (!node.IsMap() || node.size() != 10)
            return false;

        rhs.core        = node["core"].as<QString>();
        rhs.current     = node["current"].as<repository_table::current_t>();
        rhs.flash       = node["flash"].as<float>();
        rhs.frequency   = node["frequency"].as<float>();
        rhs.io          = node["io"].as<int>();
        rhs.package     = node["package"].as<QString>();
        rhs.peripherals = node["peripherals"].as<QMap<QString, int>>();
        rhs.ram         = node["ram"].as<float>();
        rhs.temperature = node["temperature"].as<repository_table::temperature_t>();
        rhs.voltage     = node["voltage"].as<repository_table::voltage_t>();
        return true;
    }
};
}  // namespace YAML

#endif  // COMMON_REPO_REPOSITORY_TABLE_H
