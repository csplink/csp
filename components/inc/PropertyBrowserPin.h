/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        PropertyBrowserPin.h
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
 *  2023-06-17     xqyjlj       initial version
 */

#ifndef PROPERTY_BROWSER_PIN_H
#define PROPERTY_BROWSER_PIN_H

#include <qttreepropertybrowser.h>
#include <qtvariantproperty.h>

#include "InterfaceGraphicsItemPin.h"
#include "Project.h"

class PropertyBrowserPin final : public QtTreePropertyBrowser
{
    Q_OBJECT
  public:
    explicit PropertyBrowserPin(QWidget *parent = nullptr);
    ~PropertyBrowserPin() override;

  private:
    enum
    {
        PROPERTY_ID_FUNCTION_TYPE = 0,
        PROPERTY_ID_PARAMETER_NAME
    };

  public slots:
    /**
     * @brief update property by pin
     * @param item: pin item
     */
    void updatePropertyByPin(QGraphicsItem *item);
    void pinValueChangedCallback(const QtProperty *property, const QVariant &value) const;
    void pinAttributeChangedCallback(const QtProperty *property, const QString &attribute, const QVariant &value) const;

  private:
    Project *projectInstance_;
    QtVariantPropertyManager *variantManager_ = new QtVariantPropertyManager(this);
    QtVariantEditorFactory *variantFactory_ = new QtVariantEditorFactory(this);
    QString pinName_ = QString();

    QtProperty *setPinBase(const QString &name, const QString &comment, int position, bool locked) const;
    QtProperty *setPinSystem(const QString &function) const;
};

#endif /** PROPERTY_BROWSER_PIN_H */
