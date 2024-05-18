/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        QtJson.h
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
 *  2023-12-03     xqyjlj       initial version
 */

#ifndef QT_JSON_H
#define QT_JSON_H

#include <QList>
#include <QMap>
#include <QPair>
#include <QString>
#include <QVector>

#include <nlohmann/json.hpp>

#define QT_JSON_EXPAND NLOHMANN_JSON_EXPAND

#define QT_JSON_PASTE  NLOHMANN_JSON_PASTE

#define QT_JSON_TO     NLOHMANN_JSON_TO

#define QT_JSON_FROM   NLOHMANN_JSON_FROM

#define QT_JSON        nlohmann

#ifndef QT_JSON_MAYBE_UNUSED_LIST
# define QT_JSON_MAYBE_UNUSED_LIST {};
#endif /** QT_JSON_MAYBE_UNUSED_LIST */

#define QT_JSON_FROM_MAYBE_UNUSED(v1)                                                                                  \
    if (JsonMaybeUnusedList.contains(#v1) && !nlohmann_json_j.contains(#v1))                                           \
    {                                                                                                                  \
        nlohmann_json_t.v1 = decltype(nlohmann_json_t.v1)();                                                           \
    }                                                                                                                  \
    else                                                                                                               \
    {                                                                                                                  \
        QT_JSON_FROM(v1);                                                                                              \
    }

#define QT_JSON_GEN_PARSE_CODE(Type, ...)                                                                              \
    inline void to_json(nlohmann::json &nlohmann_json_j, const Type &nlohmann_json_t)                                  \
    {                                                                                                                  \
        QT_JSON_EXPAND(QT_JSON_PASTE(QT_JSON_TO, __VA_ARGS__))                                                         \
    }                                                                                                                  \
    inline void from_json(const nlohmann::json &nlohmann_json_j, Type &nlohmann_json_t)                                \
    {                                                                                                                  \
        static QStringList JsonMaybeUnusedList = QT_JSON_MAYBE_UNUSED_LIST;                                            \
        QT_JSON_EXPAND(QT_JSON_PASTE(QT_JSON_FROM_MAYBE_UNUSED, __VA_ARGS__))                                          \
    }

namespace QT_JSON
{
template <> struct adl_serializer<QString>
{
    static void to_json(json &j, const QString &rhs)
    {
        j = rhs.toStdString();
    }

    static void from_json(const json &j, QString &rhs)
    {
        if (!j.is_string())
        {
            throw detail::type_error::create(302, detail::concat("type must be string, but is ", j.type_name()), &j);
        }
        rhs = QString::fromStdString(j.get<std::string>());
    }
};

template <typename T> struct adl_serializer<QMap<QString, T>>
{
    static void to_json(json &j, const QMap<QString, T> &rhs)
    {
        if (rhs.isEmpty())
        {
            j = json::object_t();
        }
        else
        {
            auto it = rhs.constBegin();
            while (it != rhs.constEnd())
            {
                j.emplace(it.key().toStdString(), it.value());
                ++it;
            }
        }
    }

    static void from_json(const json &j, QMap<QString, T> &rhs)
    {
        if (!j.is_object())
        {
            throw detail::type_error::create(302, detail::concat("type must be object, but is ", j.type_name()), &j);
        }
        rhs.clear();
        for (auto it = j.begin(); it != j.end(); ++it)
        {
            rhs.insert(QString::fromStdString(it.key()), it.value());
        }
    }
};

template <typename T> struct adl_serializer<QVector<T>>
{
    static void to_json(json &j, const QVector<T> &rhs)
    {
        if (rhs.isEmpty())
        {
            j = json::array_t();
        }
        else
        {
            QVectorIterator<T> it(rhs);

            while (it.hasNext())
            {
                j.emplace_back(it.next());
            }
        }
    }

    static void from_json(const json &j, QVector<T> &rhs)
    {
        if (!j.is_array())
        {
            throw detail::type_error::create(302, detail::concat("type must be array, but is ", j.type_name()), &j);
        }
        rhs.clear();
        for (const auto &it : j)
        {
            rhs.push_back(it);
        }
    }
};

template <typename T> struct adl_serializer<QList<T>>
{
    static void to_json(json &j, const QList<T> &rhs)
    {
        if (rhs.isEmpty())
        {
            j = json::array_t();
        }
        else
        {
            QListIterator<T> it(rhs);

            while (it.hasNext())
            {
                j.emplace_back(it.next());
            }
        }
    }

    static void from_json(const json &j, QList<T> &rhs)
    {
        if (!j.is_array())
        {
            throw detail::type_error::create(302, detail::concat("type must be array, but is ", j.type_name()), &j);
        }
        rhs.clear();
        for (const auto &it : j)
        {
            rhs.push_back(it);
        }
    }
};

template <> struct adl_serializer<QStringList>
{
    static void to_json(json &j, const QStringList &rhs)
    {
        if (rhs.isEmpty())
        {
            j = json::array_t();
        }
        else
        {
            QStringListIterator it(rhs);

            while (it.hasNext())
            {
                j.emplace_back(it.next());
            }
        }
    }

    static void from_json(const json &j, QStringList &rhs)
    {
        if (!j.is_array())
        {
            throw detail::type_error::create(302, detail::concat("type must be array, but is ", j.type_name()), &j);
        }
        rhs.clear();
        for (const auto &it : j)
        {
            rhs.push_back(it);
        }
    }
};

} // namespace QT_JSON

#define QT_DEBUG_ADD_TYPE(Type)                                                                                        \
    QDebug operator<<(QDebug debug, const Type &rhs)                                                                   \
    {                                                                                                                  \
        const nlohmann::json j = rhs;                                                                                  \
        debug << QString::fromStdString(j.dump(2));                                                                    \
        return debug;                                                                                                  \
    }

#endif /** QT_JSON_H */
