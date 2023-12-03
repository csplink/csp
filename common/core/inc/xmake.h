/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        xmake.h
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
 *  2023-08-14     xqyjlj       initial version
 */

#ifndef CSP_COMMON_CORE_XMAKE_H
#define CSP_COMMON_CORE_XMAKE_H

#include "os.h"
#include "qtjson.h"
#include "qtyaml.h"

class xmake final
{
  public:
    typedef struct info_struct
    {
        QMap<QString, QString> versions;
        QStringList urls;
        QString homepage;
        QString description;
        QString license;
    } info_t;

    typedef QMap<QString, info_t> package_t;

    typedef struct packages_struct
    {
        package_t toolchain;
        package_t library;
    } packages_t;

  public:
    /**
     * @brief get xmake version
     * @param program: program path or name
     * @return version; <example: "v2.7.9+HEAD.c879226">
     */
    static QString version(const QString &program = "xmake");

    /**
     * @brief run the lua script.
     * @param lua_path: lua path
     * @param args: args
     * @param program: program path or name
     * @param workdir: working directory
     * @return lua output
     */
    static QString lua(const QString &lua_path, const QStringList &args = {}, const QString &program = "xmake",
                       const QString &workdir = "");

    /**
     * @brief get package configuration from file
     * @param file: json file path
     * @return xmake:packages_t
     */
    static packages_t load_packages_byfile(const QString &file);

    /**
     * @brief get package configuration from csp repo
     * @param program: xmake exe path
     * @param workdir: xmake workdir
     * @return xmake:packages_t
     */
    static packages_t load_packages(const QString &program = "xmake", const QString &workdir = "");

  private:
    xmake() = default;
    ~xmake() = default;

    Q_DISABLE_COPY_MOVE(xmake)
};

namespace YAML
{
template <> struct convert<xmake::info_t>
{
    static Node encode(const xmake::info_t &rhs)
    {
        Node node;
        node.force_insert("versions", rhs.versions);
        node.force_insert("urls", rhs.urls);
        node.force_insert("homepage", rhs.homepage);
        node.force_insert("description", rhs.description);
        node.force_insert("license", rhs.license);
        return node;
    }

    static bool decode(const Node &node, xmake::info_t &rhs)
    {
        if (!node.IsMap() || node.size() < 2)
            return false;

        rhs.versions = node["versions"].as<QMap<QString, QString>>();
        rhs.urls = node["urls"].as<QStringList>();
        rhs.homepage = node["homepage"].as<QString>();
        rhs.description = node["description"].as<QString>();
        rhs.license = node["license"].as<QString>();
        return true;
    }
};

template <> struct convert<xmake::packages_t>
{
    static Node encode(const xmake::packages_t &rhs)
    {
        Node node;
        node.force_insert("toolchain", rhs.toolchain);
        node.force_insert("library", rhs.library);
        return node;
    }

    static bool decode(const Node &node, xmake::packages_t &rhs)
    {
        if (!node.IsMap() || node.size() < 2)
            return false;

        rhs.toolchain = node["toolchain"].as<xmake::package_t>();
        rhs.library = node["library"].as<xmake::package_t>();
        return true;
    }
};
} // namespace YAML

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(xmake::info_struct, versions, urls, homepage, description, license)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(xmake::packages_struct, toolchain, library)
} // namespace nlohmann

#endif //  CSP_COMMON_CORE_XMAKE_H
