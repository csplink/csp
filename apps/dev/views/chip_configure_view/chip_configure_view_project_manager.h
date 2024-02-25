/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        chip_configure_view_project_manager.h
 * @brief
 *
 *****************************************************************************
 * @attention
 * Licensed under the GNU General Public License v. 3 (the "License");
 * You may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.gnu.org/licenses/gpl-3.0.html
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Copyright (C) 2024-2024 xqyjlj<xqyjlj@126.com>
 *
 *****************************************************************************
 * Change Logs:
 * Date           Author       Notes
 * ------------   ----------   -----------------------------------------------
 * 2024-02-22     xqyjlj       initial version
 */

#ifndef CHIP_CONFIGURE_VIEW_PROJECT_MANAGER_H
#define CHIP_CONFIGURE_VIEW_PROJECT_MANAGER_H

#include <QWidget>

#include "project.h"

namespace Ui
{
class chip_configure_view_project_manager;
}

class chip_configure_view_project_manager final : public QWidget
{
    Q_OBJECT

  public:
    explicit chip_configure_view_project_manager(QWidget *parent = nullptr);
    ~chip_configure_view_project_manager() override;

  private:
    Ui::chip_configure_view_project_manager *_ui;
    project *_project_instance;

    void init_project_settings() const;
    void init_linker_settings() const;
    void init_package_settings() const;
};

#endif // CHIP_CONFIGURE_VIEW_PROJECT_MANAGER_H
