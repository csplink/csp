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

#include "ip_table.h"
#include "project_table.h"

namespace csp {
class project : public QObject {
    Q_OBJECT

public:
    QString                      get_core(const QString &key) const;
    void                         set_core(const QString &key, const QString &value);
    QString                      get_path() const;
    void                         set_path(const QString &path);
    project_table::pin_config_t &get_pin_config(const QString &key);
    ip_table::ips_t             &load_ips(const QString &hal, const QString &name);
    ip_table::ips_t             &get_ips();

private:
    project_table::project_t _project;
    QString                  _path;
    ip_table::ips_t          _ips;

public:
    static project *get_instance();

private:
    project();
    ~project() override;

    project(const project &signal);
    const project &operator=(const project &signal);

private:
    static project *_instance;
};
}  // namespace csp
#endif  // COMMON_PROJECT_CSP_PROJECT_H
