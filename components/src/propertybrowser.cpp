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
#include "os.h"
#include "pinout_table.h"
#include "propertybrowser.h"

propertybrowser::propertybrowser(QWidget *parent) : QtTreePropertyBrowser(parent)
{
    _project_instance = project::get_instance();
}

propertybrowser::~propertybrowser() = default;

QtProperty *propertybrowser::set_pin_base(const QString &name, const QString &comment, const int position,
                                          const bool locked) const
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

QtProperty *propertybrowser::set_pin_system(const QString &function) const
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
    disconnect(_variant_manager, &QtVariantPropertyManager::attributeChanged, this, nullptr);

    this->clear();
    const auto pin = dynamic_cast<interface_graphicsitem_pin *>(item);
    const auto name = pin->objectName();
    const auto pinout_unit =
        pin->property(interface_graphicsitem_pin::property_name_pinout_unit_ptr).value<pinout_table::pinout_unit_t *>();
    if (pinout_unit == nullptr)
        return;

    const auto function = _project_instance->get_pin_function(name);            // such as "GPIO-Input"
    const auto comment = _project_instance->get_pin_comment(name);              // such as "LED0"
    const auto locked = _project_instance->get_pin_locked(name);                // such as "true"
    const auto function_type = pinout_unit->functions[function].type.toLower(); // such as "gpio"
    const auto maps = _project_instance->get_maps();

    const auto base_group_item = set_pin_base(name, comment, pinout_unit->position, locked);
    this->addProperty(base_group_item);
    const auto function_group_item = set_pin_system(function);
    this->addProperty(function_group_item);

    if (maps.contains(function_type))
    {
        auto map = _project_instance->get_maps()[function_type];          // such as "map/gpio.yml"
        const auto fps = _project_instance->get_pin_config_fps(name);     // ping config function properties
        const auto function_mode = pinout_unit->functions[function].mode; // such as "Input-Std <just string>"
        auto ip = _project_instance->get_ips()[function_type];            // such as "apm32f103zet6/ip/gpio.yml"
        const auto ip_map = ip[function_mode];                            // such as "Input-Std <just struct>"
        auto ip_map_i = ip_map.constBegin();
        const auto type = pinout_unit->functions[function].type; // such as "GPIO"
        QtProperty *group_item = _variant_manager->addProperty(QtVariantPropertyManager::groupTypeId(), type);
        project_table::pin_function_property_t fp = {};

        if (fps.contains(function_type)) // already configured
            fp = fps.value(function_type);

        _project_instance->clear_pin_config_fp_module(name, function_type); // clear properties module

        while (ip_map_i != ip_map.constEnd())
        {
            auto parameter_name = ip_map_i.key();                // such as "chal_gpio_pull_t <just string>"
            auto parameters = ip_map_i.value();                  // such as "CHAL_GPIO_PULL_UP, CHAL_GPIO_PULL_DOWN"
            auto property = map.properties[parameter_name];      // such as "chal_gpio_pull_t <just struct>"
            auto language = config::language();                  // such as "zh_CN"
            auto display_name = property.display_name[language]; // such as "钳位<zh_CN>, means PULL<en>"
            auto description = property.description[language];   // such as "GPIO-钳位<zh_CN>, means GPIO-PULL<en>"
            const auto id = QtVariantPropertyManager::enumTypeId();
            auto *variant_item = _variant_manager->addProperty(id, display_name);
            QStringList values;
            for (const auto &parameter : parameters)
            {
                values.append(map.total[parameter]); // such as "上拉, 下拉"
            }
            variant_item->setAttribute("enumNames", values);

            if (!fp.isEmpty()) // already configured
            {
                auto value = map.total.value(fp.value(parameter_name));
                if (!value.isEmpty() && values.contains(value))
                {
                    variant_item->setValue(values.indexOf(value)); // just read
                    _project_instance->set_pin_config_fp(name, function_type, parameter_name, fp.value(parameter_name));
                }
                else
                {
                    variant_item->setValue(0); // default value
                    _project_instance->set_pin_config_fp(name, function_type, parameter_name, parameters[0]);
                }
            }
            else
            {
                variant_item->setValue(0); // default value
                _project_instance->set_pin_config_fp(name, function_type, parameter_name, parameters[0]);
            }

            variant_item->setDescriptionToolTip(description);
            variant_item->set_user_property(PROPERTY_ID_FUNCTION_TYPE, function_type);
            variant_item->set_user_property(PROPERTY_ID_PARAMETER_NAME, parameter_name);
            group_item->addSubProperty(variant_item);

            ++ip_map_i;
        }
        this->addProperty(group_item);
    }

    this->setFactoryForManager(_variant_manager, _variant_factory);

    connect(_variant_manager, &QtVariantPropertyManager::valueChanged, this,
            &propertybrowser::pin_value_changed_callback, Qt::UniqueConnection);
    connect(_variant_manager, &QtVariantPropertyManager::attributeChanged, this,
            &propertybrowser::pin_attribute_changed_callback, Qt::UniqueConnection);

    _pin_name = name;
}

void propertybrowser::pin_value_changed_callback(const QtProperty *property, const QVariant &value) const
{
    if (_pin_name.isEmpty())
        return;

    switch (const auto type = _variant_manager->propertyType(property))
    {
    case QVariant::String: {
        if (property->propertyName() == tr("Comment"))
            _project_instance->set_pin_comment(_pin_name, value.toString());

        break;
    }
    case QVariant::Bool: {
        if (property->propertyName() == tr("Locked"))
            _project_instance->set_pin_locked(_pin_name, value.toBool());

        break;
    }
    case QVariant::Int: {
        break;
    }
    default: {
        if (type == QtVariantPropertyManager::enumTypeId())
        {
            const auto property_name = property->propertyName();
            const auto function_type = property->get_user_property(PROPERTY_ID_FUNCTION_TYPE).toString();
            const auto parameter_name = property->get_user_property(PROPERTY_ID_PARAMETER_NAME).toString();
            const auto parameter_value_translations = property->valueText();
            auto total = _project_instance->get_maps()[function_type].reverse_total;
            const auto parameter_value = total[property->valueText()];

            Q_UNUSED(property_name)
            Q_UNUSED(parameter_value_translations)

            _project_instance->set_pin_config_fp(_pin_name, function_type, parameter_name, parameter_value);
        }
        else
        {
            qDebug() << _variant_manager->propertyType(property) << property << property->propertyName() << value;
        }
        break;
    }
    }
}

void propertybrowser::pin_attribute_changed_callback(const QtProperty *property, const QString &attribute,
                                                     const QVariant &value) const
{
    Q_UNUSED(property)
    Q_UNUSED(attribute)
    Q_UNUSED(value)
}
