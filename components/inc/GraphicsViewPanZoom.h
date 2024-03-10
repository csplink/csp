/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        GraphicsViewPanZoom.h
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

#ifndef GRAPHICS_VIEW_PAN_ZOOM_H
#define GRAPHICS_VIEW_PAN_ZOOM_H

#include <QGraphicsView>
#include <QKeyEvent>

class GraphicsViewPanZoom final : public QGraphicsView
{
    Q_OBJECT

  public:
    explicit GraphicsViewPanZoom(QWidget *parent = nullptr);
    ~GraphicsViewPanZoom() override;

    /**
     * @brief zoom in
     * @param value: zoom value
     */
    void zoomIn(int value);

    /**
     * @brief zoom out
     * @param value: zoom value
     */
    void zoomOut(int value);

    void zoom(qreal value);

    void resize();

  private:
    /**
     * @brief resizing via setup matrix
     */
    void setupMatrix();

  signals:
    /**
     * @brief selected item changed
     * @param item: selected item
     */
    void signalsSelectedItemClicked(QGraphicsItem *item);

  public:
    void propertyChangedCallback(QGraphicsItem *item);

  protected:
    void mousePressEvent(QMouseEvent *event) override;
    void mouseMoveEvent(QMouseEvent *event) override;
    void mouseReleaseEvent(QMouseEvent *event) override;
    void wheelEvent(QWheelEvent *event) override;
    void contextMenuEvent(QContextMenuEvent *event) override;

  private:
    qreal scale_;
    bool isPressed_ = false;
};

#endif /** GRAPHICS_VIEW_PAN_ZOOM_H */
