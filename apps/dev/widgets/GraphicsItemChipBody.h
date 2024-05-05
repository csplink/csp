/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        GraphicsItemChipBody.h
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
 *  2023-06-05     xqyjlj       initial version
 */

#ifndef __GRAPHICS_ITEM_CHIP_BODY_H__
#define __GRAPHICS_ITEM_CHIP_BODY_H__

#include <QGraphicsItem>
#include <QPainter>

class GraphicsItemChipBody final : public QGraphicsItem
{
  public:
    explicit GraphicsItemChipBody(qreal width, qreal height, const QString &name, const QString &company,
                                  const QString &package);
    ~GraphicsItemChipBody() override;

  private:
    qreal m_width;
    qreal m_height;
    QString m_name;
    QString m_company;
    QString m_package;
    QFont *m_font;

  protected:
    QRectF boundingRect() const override;
    QPainterPath shape() const override;
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget) override;
};

#endif /** __GRAPHICS_ITEM_CHIP_BODY_H__ */
