/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        qtyaml.h
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
 *  2023-04-19     xqyjlj       initial version
 */

#ifndef COMMON_COMPAT_LAYER_QTYAML_H
#define COMMON_COMPAT_LAYER_QTYAML_H

#include <iostream>
#include <QtCore/QList>
#include <QtCore/QMap>
#include <QtCore/QPair>
#include <QtCore/QString>
#include <QtCore/QVector>
#include <type_traits>

#include <yaml-cpp/yaml.h>

namespace YAML {

// QString
template <> struct convert<QString>
{
    static Node encode(const QString &rhs)
    {
        return Node(rhs.toStdString());
    }

    static bool decode(const Node &node, QString &rhs)
    {
        if (!node.IsScalar())
            return false;
        rhs = QString::fromStdString(node.Scalar());
        return true;
    }
};

// QMap
template <typename Key, typename Value> struct convert<QMap<Key, Value>>
{
    static Node encode(const QMap<Key, Value> &rhs)
    {
        Node node(NodeType::Map);
        auto it = rhs.constBegin();
        while (it != rhs.constEnd())
        {
            node.force_insert(it.key(), it.value());
            ++it;
        }
        return node;
    }

    static bool decode(const Node &node, QMap<Key, Value> &rhs)
    {
        if (!node.IsMap())
            return false;

        rhs.clear();
        const_iterator it = node.begin();
        while (it != node.end())
        {
            if (it->second.IsNull())
                rhs[it->first.as<Key>()] = Value();
            else
                rhs[it->first.as<Key>()] = it->second.as<Value>();
            ++it;
        }
        return true;
    }
};

// QVector
template <typename T> struct convert<QVector<T>>
{
    static Node encode(const QVector<T> &rhs)
    {
        Node node(NodeType::Sequence);
        for (T &value : rhs)
        {
            node.push_back(value);
        }
        return node;
    }

    static bool decode(const Node &node, QVector<T> &rhs)
    {
        if (!node.IsSequence())
            return false;

        rhs.clear();
        const_iterator it = node.begin();
        while (it != node.end())
        {
            rhs.push_back(it->as<T>());
            ++it;
        }
        return true;
    }
};

// QList
template <typename T> struct convert<QList<T>>
{
    static Node encode(const QList<T> &rhs)
    {
        Node node(NodeType::Sequence);
        for (T &value : rhs)
        {
            node.push_back(value);
        }
        return node;
    }

    static bool decode(const Node &node, QList<T> &rhs)
    {
        if (!node.IsSequence())
            return false;

        rhs.clear();
        const_iterator it = node.begin();
        while (it != node.end())
        {
            rhs.push_back(it->as<T>());
            ++it;
        }
        return true;
    }
};

// QPair
template <typename T, typename U> struct convert<QPair<T, U>>
{
    static Node encode(const QPair<T, U> &rhs)
    {
        Node node(NodeType::Sequence);
        node.push_back(rhs.first);
        node.push_back(rhs.second);
        return node;
    }

    static bool decode(const Node &node, QPair<T, U> &rhs)
    {
        if (!node.IsSequence())
            return false;
        if (node.size() != 2)
            return false;

        rhs.first  = node[0].as<T>();
        rhs.second = node[1].as<U>();
        return true;
    }
};

// QStringList
template <> struct convert<QStringList>
{
    static Node encode(const QStringList &rhs)
    {
        Node node(NodeType::Sequence);
        for (const auto &value : rhs)
        {
            node.push_back(value);
        }
        return node;
    }

    static bool decode(const Node &node, QStringList &rhs)
    {
        if (!node.IsSequence())
            return false;

        rhs.clear();
        const_iterator it = node.begin();
        while (it != node.end())
        {
            rhs.push_back(it->as<QString>());
            ++it;
        }
        return true;
    }
};

// TODO: QLinkedList, QStack, QQueue, QSet, QMultiMap, QHash, QMultiHash, ...

}  // end namespace YAML

#endif  // COMMON_COMPAT_LAYER_QTYAML_H
