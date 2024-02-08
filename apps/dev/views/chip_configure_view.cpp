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

#include <QtCore>

#include "chip_configure_view.h"
#include "lqfp.h"
#include "ui_chip_configure_view.h"

chip_configure_view::chip_configure_view(QWidget *parent) : QWidget(parent), _ui(new Ui::chip_configure_view)
{
    _ui->setupUi(this);
    _project_instance = project::get_instance();
}

chip_configure_view::~chip_configure_view()
{
    delete _ui;
}

void chip_configure_view::showEvent(QShowEvent *event)
{
    Q_UNUSED(event);
}

void chip_configure_view::set_propertybrowser(propertybrowser *instance)
{
    _propertybrowser_instance = instance;

    (void)connect(_ui->graphicsview, &graphicsview_panzoom::signals_selected_item_clicked, _propertybrowser_instance,
                  &propertybrowser::update_property_by_pin);
}

void chip_configure_view::init_view()
{
    const auto package = _project_instance->get_core(project::CORE_ATTRIBUTE_TYPE_PACKAGE).toLower();
    const auto hal = _project_instance->get_core(project::CORE_ATTRIBUTE_TYPE_HAL).toLower();
    const auto company = _project_instance->get_core(project::CORE_ATTRIBUTE_TYPE_COMPANY);
    const auto name = _project_instance->get_core(project::CORE_ATTRIBUTE_TYPE_TARGET);

    delete _ui->graphicsview->scene();
    const auto graphicsscene = new QGraphicsScene(_ui->graphicsview);
    if (package.startsWith("lqfp"))
    {
        lqfp lqfp(nullptr);
        auto items = lqfp.get_lqfp(hal, company, name);
        for (const auto &item : items)
        {
            graphicsscene->addItem(item);
            if ((item->flags() & QGraphicsItem::ItemIsFocusable) == QGraphicsItem::ItemIsFocusable)
            {
                (void)connect(dynamic_cast<const graphicsitem_pin *>(item), &graphicsitem_pin::signal_property_changed,
                              _ui->graphicsview, &graphicsview_panzoom::property_changed_callback,
                              Qt::UniqueConnection);
            }
        }
    }
    _ui->graphicsview->setScene(graphicsscene);
}

void chip_configure_view::resizeEvent(QResizeEvent *event)
{
    if (resize_counter <= 2)
    {
        resize_view();

        /**
         * 0: 视图初始化
         * 1: 布局初始化
         * 2: 全局最大化
         */
        resize_counter++;
    }
    QWidget::resizeEvent(event);
}

void chip_configure_view::resize_view() const
{
    const qreal graphicsscene_width = _ui->graphicsview->scene()->itemsBoundingRect().width();
    const qreal graphicsscene_height = _ui->graphicsview->scene()->itemsBoundingRect().height();
    const qreal view_width = static_cast<qreal>(this->_ui->graphicsview->width());
    const qreal view_height = static_cast<qreal>(this->_ui->graphicsview->height());
    const qreal scene_max = graphicsscene_width > graphicsscene_height ? graphicsscene_width : graphicsscene_height;
    const qreal view_min = view_width > view_height ? view_height : view_width;

    _ui->graphicsview->centerOn(_ui->graphicsview->scene()->itemsBoundingRect().width() / static_cast<qreal>(2),
                                _ui->graphicsview->scene()->itemsBoundingRect().height() / static_cast<qreal>(2));

    const qreal scale = view_min / scene_max;
    _ui->graphicsview->zoom(scale);
}
