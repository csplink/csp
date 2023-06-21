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
#include <QVariant>

#include "ip_table.h"
#include "map_table.h"
#include "project_table.h"

class project : public QObject {
    Q_OBJECT

public:
    /******************* core ***********************/
    /**
     * @brief get core config value by core name
     * @param key: core name
     * @return core config value
     */
    QString get_core(const QString &key) const;

    /**
     * @brief set core config value by core name
     * @param key: core name
     * @param value: core config value
     */
    void set_core(const QString &key, const QString &value);
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
     * @brief load ip map from db
     * @param hal: hal name
     * @param name: chip name
     * @return ip map as a modifiable reference
     */
    ip_table::ips_t &load_ips(const QString &hal, const QString &name);

    /**
     * @brief get ip map
     * @return ip map as a modifiable reference
     */
    ip_table::ips_t &get_ips();

    /**
     * @brief load hal map from db
     * @param hal: hal name
     * @param name: chip name
     * @return hal map as a modifiable reference
     */
    map_table::maps_t &load_maps(const QString &hal);

    /**
     * @brief get hal map
     * @return hal map as a modifiable reference
     */
    map_table::maps_t &get_maps();
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

    /***********************************************/
private:
    project_table::project_t _project;  // project table
    QString                  _path;     // project file path
    ip_table::ips_t          _ips;      // ip map
    map_table::maps_t        _maps;     // hal map

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
    void signals_pin_property_changed(const QString  &property,
                                      const QString  &name,
                                      const QVariant &old_value,
                                      const QVariant &new_value);

private:
    project();
    ~project() override;

    project(const project &signal);
    const project &operator=(const project &signal);

private:
    static project *_instance;
};

#endif  // COMMON_PROJECT_CSP_PROJECT_H
