/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        propertybrowser.h
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

#ifndef CSP_PROPERTYBROWSER_H
#define CSP_PROPERTYBROWSER_H

#include "qtvariantproperty.h"
#include <qtpropertymanager.h>
#include <qttreepropertybrowser.h>

#include "interface_graphicsitem_pin.h"
#include "project.h"

class propertybrowser final : public QtTreePropertyBrowser
{
    Q_OBJECT
  public:
    explicit propertybrowser(QWidget *parent = nullptr);
    ~propertybrowser() override;

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
    void update_property_by_pin(QGraphicsItem *item);
    void pin_value_changed_callback(const QtProperty *property, const QVariant &value) const;
    void pin_attribute_changed_callback(const QtProperty *property, const QString &attribute, const QVariant &value) const;

  private:
    QtProperty *set_pin_base(const QString &name, const QString &comment, int position, bool locked) const;
    QtProperty *set_pin_system(const QString &function) const;

  private:
    project *_project_instance;
    QtVariantPropertyManager *_variant_manager = new QtVariantPropertyManager(this);
    QtVariantEditorFactory *_variant_factory = new QtVariantEditorFactory(this);
    QString _pin_name = QString();
};

#endif // CSP_PROPERTYBROWSER_H
