/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        chip_configure_view.cpp
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
 *  2023-05-14     xqyjlj       initial version
 */

#include <QDebug>
#include <QOpenGLWidget>
#include <QtCore>

#include "chip_configure_view.h"
#include "lqfp.h"
#include "ui_chip_configure_view.h"

chip_configure_view::chip_configure_view(QWidget *parent) : QWidget(parent), ui(new Ui::chip_configure_view)
{
    ui->setupUi(this);
    _project_instance = project::get_instance();
}

chip_configure_view::~chip_configure_view()
{
    delete ui;
}

void chip_configure_view::showEvent(QShowEvent *event)
{
    Q_UNUSED(event);
}

void chip_configure_view::set_propertybrowser(propertybrowser *instance)
{
    _propertybrowser_instance = instance;

    connect(ui->graphicsview, &graphicsview_panzoom::signals_selected_item_clicked, _propertybrowser_instance,
            &propertybrowser::update_property_by_pin);
}

void chip_configure_view::init_view()
{
    auto package = _project_instance->get_core(CSP_PROJECT_CORE_PACKAGE).toLower();
    auto hal     = _project_instance->get_core(CSP_PROJECT_CORE_HAL).toLower();
    auto company = _project_instance->get_core(CSP_PROJECT_CORE_COMPANY);
    auto name    = _project_instance->get_core(CSP_PROJECT_CORE_HAL_NAME);

    auto graphicsscene = new QGraphicsScene(ui->graphicsview);
    if (package.startsWith("lqfp"))
    {
        lqfp lqfp(nullptr);

        auto items = lqfp.get_lqfp(hal, company, name);
        for (auto &item : items)
        {
            graphicsscene->addItem(item);
            if (item->flags() & QGraphicsItem::ItemIsFocusable)
            {
                connect(dynamic_cast<graphicsitem_pin *>(item), &graphicsitem_pin::signal_property_changed,
                        ui->graphicsview, &graphicsview_panzoom::property_changed_callback, Qt::UniqueConnection);
            }
        }
    }
    ui->graphicsview->setScene(graphicsscene);
}
