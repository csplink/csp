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

#include "config.h"
#include "propertybrowser.h"

propertybrowser::propertybrowser(QWidget *parent) : QtTreePropertyBrowser(parent)
{
    _project_instance = project::get_instance();
}

propertybrowser::~propertybrowser() = default;

QtProperty *propertybrowser::set_pin_base(const QString &name, const QString &comment, int position, bool locked)
{
    auto *group_item = _variant_manager->addProperty(QtVariantPropertyManager::groupTypeId(), tr("Base"));

    auto *variant_item = _variant_manager->addProperty(QVariant::Bool, tr("Locked"));
    variant_item->setValue(locked);
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
    auto *group_item = _variant_manager->addProperty(QtVariantPropertyManager::groupTypeId(), tr("System"));

    auto *variant_item = _variant_manager->addProperty(QVariant::String, tr("Function"));
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
    auto locked        = _project_instance->get_pin_locked(name);
    auto function_type = pinout_unit->functions[function].type.toLower();
    auto maps          = _project_instance->get_maps();

    auto base_group_item = set_pin_base(name, comment, pinout_unit->position, locked);
    this->addProperty(base_group_item);
    auto function_group_item = set_pin_system(function);
    this->addProperty(function_group_item);

    if (maps.contains(function_type))
    {
        auto        map           = _project_instance->get_maps()[function_type];
        auto        function_mode = pinout_unit->functions[function].mode;
        auto        ip            = _project_instance->get_ips()[function_type];
        auto        ip_map        = ip[function_mode];
        auto        ip_map_i      = ip_map.constBegin();
        auto        type          = pinout_unit->functions[function].type;
        QtProperty *group_item    = _variant_manager->addProperty(QtVariantPropertyManager::groupTypeId(), type);
        while (ip_map_i != ip_map.constEnd())
        {
            auto parameter_name = ip_map_i.key();
            auto parameters     = ip_map_i.value();
            auto property       = map.properties[parameter_name];
            auto language       = config::language();

            auto *variant_item =
                _variant_manager->addProperty(QtVariantPropertyManager::enumTypeId(), property.display_name[language]);
            QStringList values;
            for (const auto &parameter : parameters)
            {
                values.append(map.total[parameter]);
            }
            variant_item->setAttribute("enumNames", values);
            variant_item->setDescriptionToolTip(property.description[language]);
            group_item->addSubProperty(variant_item);

            ip_map_i++;
        }
        this->addProperty(group_item);
    }

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
    else if (property->propertyName() == tr("Locked"))
        _project_instance->set_pin_locked(_pin_name, value.toBool());
    else
        qDebug() << property << property->propertyName() << value;
}
