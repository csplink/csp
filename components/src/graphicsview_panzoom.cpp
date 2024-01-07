/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        graphicsview_panzoom.cpp
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
 *  2023-06-09     xqyjlj       initial version
 */
#include <QtCore>
#include <QtOpenGL>

#include "graphicsview_panzoom.h"
#include "interface_graphicsitem_pin.h"

static constexpr qreal min_scale = 0;
static constexpr qreal max_scale = 1000;
static constexpr qreal resolution = 50;

graphicsview_panzoom::graphicsview_panzoom(QWidget *parent) : QGraphicsView(parent)
{
    _scale = (min_scale + max_scale) / 2;

    this->setViewport(new QGLWidget(QGLFormat(QGL::SampleBuffers)));
    this->setDragMode(QGraphicsView::ScrollHandDrag);
    this->setInteractive(false);
    this->setAcceptDrops(false);
    this->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    this->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    this->setOptimizationFlags(QGraphicsView::DontSavePainterState);
    this->setViewportUpdateMode(QGraphicsView::SmartViewportUpdate);
    this->setRenderHints(QPainter::Antialiasing | QPainter::TextAntialiasing | QPainter::SmoothPixmapTransform |
                         QPainter::Qt4CompatiblePainting | QPainter::LosslessImageRendering);
    this->viewport()->setCursor(Qt::ArrowCursor);
    this->setSceneRect(INT_MIN / 2, INT_MIN / 2, INT_MAX, INT_MAX);
}

graphicsview_panzoom::~graphicsview_panzoom() = default;

void graphicsview_panzoom::setup_matrix()
{
    const qreal scale = qPow(2, (_scale - (min_scale + max_scale) / 2) / resolution);
    QTransform matrix;
    matrix.scale(scale, scale);
    //    matrix.rotate(90);

    this->setTransform(matrix);
}

void graphicsview_panzoom::mousePressEvent(QMouseEvent *event)
{
    QGraphicsView::mousePressEvent(event);
    _is_pressed = true;
    viewport()->setCursor(Qt::ArrowCursor);

    auto *item = this->itemAt(event->pos());
    if (item == nullptr)
        return;

    if (!(item->flags() & QGraphicsItem::ItemIsFocusable))
        return;

    emit signals_selected_item_clicked(item);
}

void graphicsview_panzoom::mouseMoveEvent(QMouseEvent *event)
{
    QGraphicsView::mouseMoveEvent(event);

    if (_is_pressed)
        viewport()->setCursor(Qt::ClosedHandCursor);
}

void graphicsview_panzoom::mouseReleaseEvent(QMouseEvent *event)
{
    QGraphicsView::mouseReleaseEvent(event);
    _is_pressed = false;
    viewport()->setCursor(Qt::ArrowCursor);
}

void graphicsview_panzoom::wheelEvent(QWheelEvent *event)
{
    const QPoint scroll_amount = event->angleDelta();
    if (scroll_amount.y() > 0)
        zoom_in(6);
    else
        zoom_out(6);
}

void graphicsview_panzoom::zoom_in(const int value)
{
    _scale += value;
    if (_scale >= max_scale)
        _scale = max_scale;
    setup_matrix();
}

void graphicsview_panzoom::zoom_out(const int value)
{
    _scale -= value;
    if (_scale <= min_scale)
        _scale = min_scale;
    setup_matrix();
}

void graphicsview_panzoom::zoom(const qreal value)
{
    _scale = qLn(value) / qLn(2) * resolution + (min_scale + max_scale / 2);
    if (_scale >= max_scale)
    {
        _scale = max_scale;
    }
    if (_scale <= min_scale)
    {
        _scale = min_scale;
    }
    setup_matrix();
}

void graphicsview_panzoom::contextMenuEvent(QContextMenuEvent *event)
{
    QGraphicsView::contextMenuEvent(event);
    const auto *item = dynamic_cast<interface_graphicsitem_pin *>(this->itemAt(event->pos()));
    if (item == nullptr)
        return;
    if (!(item->flags() & QGraphicsItem::ItemIsFocusable))
        return;

    const auto menu = item->property(interface_graphicsitem_pin::property_name_menu_ptr).value<QMenu *>();
    Q_ASSERT(menu != nullptr);

    menu->exec(event->globalPos());
}

void graphicsview_panzoom::property_changed_callback(QGraphicsItem *item)
{
    emit signals_selected_item_clicked(item);
}
