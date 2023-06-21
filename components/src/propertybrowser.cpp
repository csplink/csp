/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        propertybrowser.cpp
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

#include <QDebug>

#include "pinout_table.h"
#include "propertybrowser.h"

propertybrowser::propertybrowser(QWidget *parent) : QtTreePropertyBrowser(parent)
{
    _project_instance = project::get_instance();
}

propertybrowser::~propertybrowser() = default;

QtProperty *propertybrowser::set_pin_base(const QString &name, const QString &comment, int position)
{
    QtProperty *group_item = _variant_manager->addProperty(QtVariantPropertyManager::groupTypeId(), tr("Base"));

    QtVariantProperty *variant_item = _variant_manager->addProperty(QVariant::Bool, tr("Lock"));
    variant_item->setValue(true);
    group_item->addSubProperty(variant_item);

    variant_item = _variant_manager->addProperty(QVariant::String, tr("Comment"));
    variant_item->setValue(comment);
    group_item->addSubProperty(variant_item);

    variant_item = _variant_manager->addProperty(QVariant::String, tr("Name"));
    variant_item->setValue(name);
    variant_item->setEnabled(false);
    group_item->addSubProperty(variant_item);

    variant_item = _variant_manager->addProperty(QVariant::Int, tr("Position"));
    variant_item->setValue(position);
    variant_item->setEnabled(false);
    group_item->addSubProperty(variant_item);

    return group_item;
}

QtProperty *propertybrowser::set_pin_system(const QString &function)
{
    QtProperty *group_item = _variant_manager->addProperty(QtVariantPropertyManager::groupTypeId(), tr("System"));

    QtVariantProperty *variant_item = _variant_manager->addProperty(QVariant::String, tr("Function"));
    variant_item->setValue(function);
    variant_item->setEnabled(false);
    group_item->addSubProperty(variant_item);

    return group_item;
}

void propertybrowser::update_property_by_pin(QGraphicsItem *item)
{
    disconnect(_variant_manager, &QtVariantPropertyManager::valueChanged, this, nullptr);

    this->clear();
    auto pin  = dynamic_cast<interface_graphicsitem_pin *>(item);
    auto name = pin->objectName();
    auto pinout_unit =
        pin->property(GRAPHICSITEM_PIN_PROPERTY_NAME_PINOUT_UNIT_PTR).value<pinout_table::pinout_unit_t *>();
    auto function      = _project_instance->get_pin_function(name);
    auto comment       = _project_instance->get_pin_comment(name);
    auto function_type = pinout_unit->functions[function].type.toLower();
    auto maps          = _project_instance->get_maps();
    if (maps.contains(function_type))
    {
        auto map = _project_instance->get_maps()[function_type];
        qDebug() << name << function << function_type << _project_instance->get_maps().keys() << map.properties.size();
    }

    auto base_group_item = set_pin_base(name, comment, pinout_unit->position);
    this->addProperty(base_group_item);
    auto function_group_item = set_pin_system(function);
    this->addProperty(function_group_item);

    this->setFactoryForManager(_variant_manager, _variant_factory);

    connect(_variant_manager, &QtVariantPropertyManager::valueChanged, this,
            &propertybrowser::pin_value_changed_callback, Qt::UniqueConnection);

    _pin_name = name;
}

void propertybrowser::pin_value_changed_callback(QtProperty *property, const QVariant &value)
{
    if (_pin_name.isEmpty())
        return;

    if (property->propertyName() == tr("Comment"))
        _project_instance->set_pin_comment(_pin_name, value.toString());

    qDebug() << property->propertyName() << value;
}
