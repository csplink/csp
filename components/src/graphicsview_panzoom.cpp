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

#define MIN_SCALE 0
#define MAX_SCALE 1000

using namespace csp;

graphicsview_panzoom::graphicsview_panzoom(QWidget *parent) : QGraphicsView(parent)
{
    _scale = (MIN_SCALE + MAX_SCALE) / 2;

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
    qreal      scale = qPow(qreal(2), (_scale - (int)((MIN_SCALE + MAX_SCALE) / 2)) / qreal(50));
    QTransform matrix;
    matrix.scale(scale, scale);
    //    matrix.rotate(90);

    this->setTransform(matrix);
}

void graphicsview_panzoom::mouseReleaseEvent(QMouseEvent *event)
{
    QGraphicsView::mouseReleaseEvent(event);
    viewport()->setCursor(Qt::ArrowCursor);
}

void graphicsview_panzoom::wheelEvent(QWheelEvent *event)
{
    QPoint scrollAmount = event->angleDelta();
    if (scrollAmount.y() > 0)
        zoom_in(6);
    else
        zoom_out(6);
}

void graphicsview_panzoom::zoom_in(int value)
{
    _scale += value;
    if (_scale >= MAX_SCALE)
        _scale = MAX_SCALE;
    setup_matrix();
}

void graphicsview_panzoom::zoom_out(int value)
{
    _scale -= value;
    if (_scale <= MIN_SCALE)
        _scale = MIN_SCALE;
    setup_matrix();
}
