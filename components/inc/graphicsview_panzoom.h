/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        graphicsview_panzoom.h
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

#ifndef CSP_GRAPHICSVIEW_PANZOOM_H
#define CSP_GRAPHICSVIEW_PANZOOM_H

#include <QGraphicsView>
#include <QKeyEvent>
#include <QMouseEvent>
#include <QWheelEvent>

#include "interface_graphicsitem_pin.h"

namespace csp {

class graphicsview_panzoom : public QGraphicsView {
    Q_OBJECT

public:
    explicit graphicsview_panzoom(QWidget *parent = nullptr);
    ~graphicsview_panzoom() override;
    void setup_matrix();
    void zoom_in(int value);
    void zoom_out(int value);

protected:
    void mouseReleaseEvent(QMouseEvent *event) override;
    void wheelEvent(QWheelEvent *event) override;
    void contextMenuEvent(QContextMenuEvent *event) override;

private:
    int _scale;
};
}  // namespace csp
#endif  // CSP_GRAPHICSVIEW_PANZOOM_H