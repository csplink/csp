/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        GraphicsViewPanZoom.cpp
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

#include "GraphicsViewPanZoom.h"
#include "InterfaceGraphicsItemPin.h"

static constexpr qreal MinScale = 0;
static constexpr qreal MaxScale = 1000;
static constexpr qreal Resolution = 50;

GraphicsViewPanZoom::GraphicsViewPanZoom(QWidget *parent)
    : QGraphicsView(parent)
{
    scale_ = (MinScale + MaxScale) / 2;

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

GraphicsViewPanZoom::~GraphicsViewPanZoom() = default;

void GraphicsViewPanZoom::setupMatrix()
{
    const qreal scale = qPow(2, (scale_ - (MinScale + MaxScale) / 2) / Resolution);
    QTransform matrix;
    matrix.scale(scale, scale);
    //    matrix.rotate(90);

    this->setTransform(matrix);
}

void GraphicsViewPanZoom::mousePressEvent(QMouseEvent *event)
{
    QGraphicsView::mousePressEvent(event);
    isPressed_ = true;
    viewport()->setCursor(Qt::ArrowCursor);

    auto *item = this->itemAt(event->pos());
    if (item != nullptr)
    {
        if (item->flags() & QGraphicsItem::ItemIsFocusable)
        {
            emit signalsSelectedItemClicked(item);
        }
    }
}

void GraphicsViewPanZoom::mouseMoveEvent(QMouseEvent *event)
{
    QGraphicsView::mouseMoveEvent(event);

    if (isPressed_)
    {
        viewport()->setCursor(Qt::ClosedHandCursor);
    }
}

void GraphicsViewPanZoom::mouseReleaseEvent(QMouseEvent *event)
{
    QGraphicsView::mouseReleaseEvent(event);
    isPressed_ = false;
    viewport()->setCursor(Qt::ArrowCursor);
}

void GraphicsViewPanZoom::wheelEvent(QWheelEvent *event)
{
    const QPoint scroll_amount = event->angleDelta();
    if (scroll_amount.y() > 0)
    {
        zoomIn(6);
    }
    else
    {
        zoomOut(6);
    }
}

void GraphicsViewPanZoom::zoomIn(const int value)
{
    scale_ += value;
    if (scale_ >= MaxScale)
    {
        scale_ = MaxScale;
    }
    setupMatrix();
}

void GraphicsViewPanZoom::zoomOut(const int value)
{
    scale_ -= value;
    if (scale_ <= MinScale)
    {
        scale_ = MinScale;
    }
    setupMatrix();
}

void GraphicsViewPanZoom::zoom(const qreal value)
{
    scale_ = qLn(value) / qLn(2) * Resolution + (MinScale + MaxScale / 2);
    if (scale_ >= MaxScale)
    {
        scale_ = MaxScale;
    }
    if (scale_ <= MinScale)
    {
        scale_ = MinScale;
    }
    setupMatrix();
}

void GraphicsViewPanZoom::resize()
{
    const QGraphicsScene *gaphicsScene = scene();
    if (gaphicsScene != nullptr)
    {
        const qreal graphicsSceneWidth = gaphicsScene->itemsBoundingRect().width();
        const qreal graphicsSceneHeight = gaphicsScene->itemsBoundingRect().height();
        const qreal viewWidth = width();
        const qreal viewHeight = height();
        const qreal sceneMax = graphicsSceneWidth > graphicsSceneHeight ? graphicsSceneWidth : graphicsSceneHeight;
        const qreal viewMin = viewWidth > viewHeight ? viewHeight : viewWidth;
        const qreal scale = viewMin / sceneMax;

        centerOn(graphicsSceneWidth / static_cast<qreal>(2), graphicsSceneHeight / static_cast<qreal>(2));
        zoom(scale);
    }
}

void GraphicsViewPanZoom::contextMenuEvent(QContextMenuEvent *event)
{
    QGraphicsView::contextMenuEvent(event);
    const auto *item = dynamic_cast<InterfaceGraphicsItemPin *>(this->itemAt(event->pos()));
    if (item != nullptr)
    {
        if (item->flags() & QGraphicsItem::ItemIsFocusable)
        {
            const auto menu = item->property(InterfaceGraphicsItemPin::property_name_menu_ptr).value<QMenu *>();
            if (menu != nullptr)
            {
                menu->exec(event->globalPos());
            }
        }
    }
}

void GraphicsViewPanZoom::propertyChangedCallback(QGraphicsItem *item)
{
    emit signalsSelectedItemClicked(item);
}
