/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        project.h
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
 *  2023-05-26     xqyjlj       initial version
 */

#ifndef COMMON_PROJECT_CSP_PROJECT_H
#define COMMON_PROJECT_CSP_PROJECT_H

#include <QObject>

#include "chip_summary_table.h"
#include "ip_table.h"
#include "map_table.h"
#include "project_table.h"

class project final : public QObject
{
    Q_OBJECT

  public:
    typedef enum
    {
        CORE_ATTRIBUTE_TYPE_HAL = 0,
        CORE_ATTRIBUTE_TYPE_TARGET,
        CORE_ATTRIBUTE_TYPE_PACKAGE,
        CORE_ATTRIBUTE_TYPE_COMPANY,
        CORE_ATTRIBUTE_TYPE_TYPE,
    } core_attribute_type;

  public:
    /**
     * @brief init config
     */
    static void init();

    /**
     * @brief deinit config
     */
    static void deinit();

    /******************* core ***********************/
    /**
     * @brief get core config value by core name
     * @param type: core attribute type
     * @return core config value
     */
    QString get_core(core_attribute_type type) const;

    /**
     * @brief set core config value by core name
     * @param type: core attribute type
     * @param value: core config value
     */
    void set_core(core_attribute_type type, const QString &value);
    /***********************************************/

    /**
     * @brief get project file path
     * @return project file path
     */
    QString get_path() const;

    /**
     * @brief set project file path
     * @param path: project file path
     */
    void set_path(const QString &path);

    /**
     * @brief get project name
     * @return project name
     */
    QString get_name() const;

    /**
     * @brief set project name
     * @param name: project name
     */
    void set_name(const QString &name);

    /**
     * @brief get ip map
     * @return ip map as a modifiable reference
     */
    ip_table::ips_t &get_ips();

    /**
     * @brief get hal map
     * @return hal map as a modifiable reference
     */
    map_table::maps_t &get_maps();

    void load_chip_summary(const QString &company, const QString &name);
    chip_summary_table::chip_summary_t &get_chip_summary();

    /******************* pin ************************/
    /**
     * @brief get pin config by pin name
     * @param key: pin name
     * @return pin config as a modifiable reference
     */
    project_table::pin_config_t &get_pin_config(const QString &key);

    /**
     * @brief set pin comment by pin name
     * @param key: pin name
     * @param comment: pin comment
     */
    void set_pin_comment(const QString &key, const QString &comment);

    /**
     * @brief get pin comment by pin name
     * @param key: pin name
     * @return pin comment as a modifiable reference
     */
    QString &get_pin_comment(const QString &key);

    /**
     * @brief set pin function by pin name
     * @param key: pin name
     * @param function: pin function
     */
    void set_pin_function(const QString &key, const QString &function);

    /**
     * @brief get pin function by pin name
     * @param key: pin name
     * @return pin function as a modifiable reference
     */
    QString &get_pin_function(const QString &key);

    /**
     * @brief set pin locked by pin name
     * @param key: pin name
     * @param locked: pin locked
     */
    void set_pin_locked(const QString &key, bool locked);

    /**
     * @brief get pin locked by pin name
     * @param key: pin name
     * @return pin locked
     */
    bool get_pin_locked(const QString &key);

    /**
     * @brief set pin config function property
     * @param key: pin name
     * @param module: module name
     * @param property: property name
     * @param value: property value
     */
    void set_pin_config_fp(const QString &key, const QString &module, const QString &property, const QString &value);

    /**
     * @brief clear pin config function property
     * @param key: pin name
     * @param module: module name
     * @param property: property name
     */
    void clear_pin_config_fp(const QString &key, const QString &module, const QString &property);

    /**
     * @brief clear pin config function module properties
     * @param key: pin name
     * @param module: module name
     */
    void clear_pin_config_fp_module(const QString &key, const QString &module);

    /**
     * @brief get pin config function properties
     * @param key: pin name
     * @return pin config function properties as a modifiable reference
     */
    project_table::pin_function_properties_t &get_pin_config_fps(const QString &key);

    /**
     * @brief get pin config function property
     * @param key: pin name
     * @param module: module name
     * @param property: property name
     * @return pin config function property as a modifiable reference
     */
    QString &get_pin_config_fp(const QString &key, const QString &module, const QString &property);

    /***********************************************/

    /**
     * @brief load project from file
     * @param path: project file path
     */
    void load_project(const QString &path);

    /**
     * @brief save project to file
     * @param path: project file path
     */
    void save_project(const QString &path);

    /**
     * @brief save project to file
     */
    void save_project();

    /**
     * @brief dump project
     * @return project string
     */
    QString dump_project();

    /**
     * @brief clear project
     */
    void clear_project();

    /**
     * @brief 生成代码
     */
    void generate_code() const;

    /**
     * @brief 构建工程
     */
    void build(const QString &mode) const;

  private:
    inline static project *_instance = nullptr;
    project_table::project_t _project; // project table
    QString _path;                     // project file path
    ip_table::ips_t _ips;              // ip map
    map_table::maps_t _maps;           // hal map
    chip_summary_table::chip_summary_t _chip_summary;

  public:
    /**
     * @brief get project instance
     * @return project instance
     */
    static project *get_instance();

  signals:
    /**
     * @brief project property changed signal
     * @param property: property name
     * @param name: pin name
     * @param old_value: old value
     * @param new_value: new value
     */
    void signals_pin_property_changed(const QString &property, const QString &name, const QVariant &old_value,
                                      const QVariant &new_value);
    void signals_pin_function_property_changed(const QString &module, const QString &property, const QString &name,
                                               const QVariant &old_value, const QVariant &new_value);
    void signals_project_clear();

  private:
    project() = default;
    ~project() override = default;

    Q_DISABLE_COPY_MOVE(project)

    /**
     * @brief load hal map from db
     * @param hal: hal name
     * @return hal map as a modifiable reference
     */
    void load_maps(const QString &hal);

    /**
     * @brief load ip map from db
     * @param hal: hal name
     * @param name: chip name
     * @return ip map as a modifiable reference
     */
    void load_ips(const QString &hal, const QString &name);

    void load_db();
};

#endif // COMMON_PROJECT_CSP_PROJECT_H
