/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        chip_configure_view_project_manager.cpp
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

#include "chip_configure_view_project_manager.h"
#include "ui_chip_configure_view_project_manager.h"

chip_configure_view_project_manager::chip_configure_view_project_manager(QWidget *parent)
    : QWidget(parent), _ui(new Ui::chip_configure_view_project_manager)
{
    _ui->setupUi(this);
    _project_instance = project::get_instance();
    init_project_settings();
    init_linker_settings();
    init_package_settings();
}

chip_configure_view_project_manager::~chip_configure_view_project_manager()
{
    delete _ui;
}

void chip_configure_view_project_manager::init_project_settings() const
{
    const chip_summary_table::target_project_t &target_project = _project_instance->get_chip_summary().target_project;
    _ui->combobox_build_script_ide->clear();
    if (target_project.xmake)
    {
        _ui->combobox_build_script_ide->addItem("xmake");
    }
    if (target_project.cmake)
    {
        _ui->combobox_build_script_ide->addItem("cmake");
    }
    if (!target_project.mdk_arm.device.isEmpty())
    {
        _ui->combobox_build_script_ide->addItem("mdk_arm");
    }
}

void chip_configure_view_project_manager::init_linker_settings() const
{
    const chip_summary_table::linker_t &linker = _project_instance->get_chip_summary().linker;
    _ui->lineedit_minimun_heap_size->clear();
    if (!linker.default_minimum_heap_size.isEmpty())
    {
        _ui->lineedit_minimun_heap_size->setText(linker.default_minimum_heap_size);
    }
    else
    {
        _ui->lineedit_minimun_heap_size->setReadOnly(true);
        _ui->lineedit_minimun_heap_size->setDisabled(true);
    }

    _ui->lineedit_minimun_stack_size->clear();
    if (!linker.default_minimum_stack_size.isEmpty())
    {
        _ui->lineedit_minimun_stack_size->setText(linker.default_minimum_stack_size);
    }
    else
    {
        _ui->lineedit_minimun_stack_size->setReadOnly(true);
        _ui->lineedit_minimun_stack_size->setDisabled(true);
    }
}

void chip_configure_view_project_manager::init_package_settings() const
{
    const chip_summary_table::chip_summary_t &chip_summary = _project_instance->get_chip_summary();

    if (!chip_summary.hal.isEmpty())
    {
        _ui->lineedit_package_name->setText(chip_summary.hal);
    }
}
