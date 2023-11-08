/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        graphicsitem_chipbody.h
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

#ifndef CSP_GRAPHICSITEM_CHIPBODY_H
#define CSP_GRAPHICSITEM_CHIPBODY_H

#include <QGraphicsItem>
#include <QPainter>

class graphicsitem_chipbody final : public QGraphicsItem
{
  public:
    explicit graphicsitem_chipbody(qreal width, qreal height, const QString &name, const QString &company,
                                   const QString &package);
    ~graphicsitem_chipbody() override;

  private:
    qreal _width;
    qreal _height;
    QString _name;
    QString _company;
    QString _package;
    QFont *_font;

  protected:
    QRectF boundingRect() const override;
    QPainterPath shape() const override;
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget) override;
};

#endif // CSP_GRAPHICSITEM_CHIPBODY_H
