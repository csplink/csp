/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        PropertyBrowserPin.cpp
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

#include "PinoutTable.h"
#include "Project.h"
#include "PropertyBrowserPin.h"
#include "Repo.h"
#include "Settings.h"

PropertyBrowserPin::PropertyBrowserPin(QWidget *parent)
    : QtTreePropertyBrowser(parent)
{
}

PropertyBrowserPin::~PropertyBrowserPin() = default;

QtProperty *PropertyBrowserPin::setPinBase(const QString &name, const QString &comment, const int position,
                                           const bool locked) const
{
    QtVariantProperty *groupItem;
    groupItem = m_variantManager->addProperty(QtVariantPropertyManager::groupTypeId(), tr("Base"));

    QtVariantProperty *variantItem = m_variantManager->addProperty(QVariant::Bool, tr("Locked"));
    variantItem->setValue(locked);
    groupItem->addSubProperty(variantItem);

    variantItem = m_variantManager->addProperty(QVariant::String, tr("Comment"));
    variantItem->setValue(comment);
    groupItem->addSubProperty(variantItem);

    variantItem = m_variantManager->addProperty(QVariant::String, tr("Name"));
    variantItem->setValue(name);
    variantItem->setEnabled(false);
    groupItem->addSubProperty(variantItem);

    variantItem = m_variantManager->addProperty(QVariant::Int, tr("Position"));
    variantItem->setValue(position);
    variantItem->setEnabled(false);
    groupItem->addSubProperty(variantItem);

    return groupItem;
}

QtProperty *PropertyBrowserPin::setPinSystem(const QString &function) const
{
    QtVariantProperty *groupItem = m_variantManager->addProperty(QtVariantPropertyManager::groupTypeId(), tr("System"));
    QtVariantProperty *variantItem = m_variantManager->addProperty(QVariant::String, tr("Function"));
    variantItem->setValue(function);
    variantItem->setEnabled(false);
    groupItem->addSubProperty(variantItem);

    return groupItem;
}

void PropertyBrowserPin::updatePropertyByPin(QGraphicsItem *item)
{
    (void)disconnect(m_variantManager, &QtVariantPropertyManager::valueChanged, this, nullptr);
    (void)disconnect(m_variantManager, &QtVariantPropertyManager::attributeChanged, this, nullptr);

    this->clear();
    const InterfaceGraphicsItemPin *pin = dynamic_cast<InterfaceGraphicsItemPin *>(item);
    const QString name = pin->objectName();
    const auto pinoutUnit =
        pin->property(InterfaceGraphicsItemPin::property_name_pinout_unit_ptr).value<PinoutTable::PinoutUnitType *>();
    if (pinoutUnit == nullptr)
    {
        return;
    }

    const QString function = Project.pinFunction(name);                          // such as "GPIO-Input"
    const QString comment = Project.pinComment(name);                            // such as "LED0"
    const bool locked = Project.pinLocked(name);                                 // such as "true"
    const QString functionType = pinoutUnit->Functions[function].Type.toLower(); // such as "gpio"
    const MapTable::MapsType maps = Repo.getMaps(Project.hal());

    const auto base_group_item = setPinBase(name, comment, pinoutUnit->Position, locked);
    this->addProperty(base_group_item);
    const auto function_group_item = setPinSystem(function);
    this->addProperty(function_group_item);

    if (maps.contains(functionType))
    {
        auto map = maps[functionType];                                   // such as "map/gpio.yml"
        const auto fps = Project.pinConfigFunctionProperty(name);        // ping config function properties
        const auto function_mode = pinoutUnit->Functions[function].Mode; // such as "Input-Std <just string>"
        const IpTable::IpsType ips = Repo.getIps(Project.hal(), Project.targetChip());
        const IpTable::IpType ip = ips[functionType];        // such as "apm32f103zet6/ip/gpio.yml"
        const IpTable::IpMapType ip_map = ip[function_mode]; // such as "Input-Std <just struct>"
        auto ip_map_i = ip_map.constBegin();
        const auto type = pinoutUnit->Functions[function].Type; // such as "GPIO"
        QtProperty *groupItem = m_variantManager->addProperty(QtVariantPropertyManager::groupTypeId(), type);
        ProjectTable::PinFunctionPropertyType fp = {};

        if (fps.contains(functionType)) // already configured
        {
            fp = fps.value(functionType);
        }

        Project.clearPinConfigFunctionProperty(name, functionType); // clear properties module

        while (ip_map_i != ip_map.constEnd())
        {
            auto parameterName = ip_map_i.key();               // such as "chal_gpio_pull_t <just string>"
            auto parameters = ip_map_i.value();                // such as "CHAL_GPIO_PULL_UP, CHAL_GPIO_PULL_DOWN"
            auto property = map.Properties[parameterName];     // such as "chal_gpio_pull_t <just struct>"
            auto language = Settings.language();               // such as "zh_CN"
            auto displayName = property.DisplayName[language]; // such as "钳位<zh_CN>, means PULL<en>"
            auto description = property.Description[language]; // such as "GPIO-钳位<zh_CN>, means GPIO-PULL<en>"
            const int id = QtVariantPropertyManager::enumTypeId();
            QtVariantProperty *variantItem = m_variantManager->addProperty(id, displayName);
            QStringList values;
            for (const auto &parameter : parameters)
            {
                values.append(map.Total[parameter]); // such as "上拉, 下拉"
            }
            variantItem->setAttribute("enumNames", values);

            if (!fp.isEmpty()) // already configured
            {
                auto value = map.Total.value(fp.value(parameterName));
                if (!value.isEmpty() && values.contains(value))
                {
                    variantItem->setValue(values.indexOf(value)); // just read
                    Project.setPinConfigFunctionProperty(name, functionType, parameterName, fp.value(parameterName));
                }
                else
                {
                    variantItem->setValue(0); // default value
                    Project.setPinConfigFunctionProperty(name, functionType, parameterName, parameters[0]);
                }
            }
            else
            {
                variantItem->setValue(0); // default value
                Project.setPinConfigFunctionProperty(name, functionType, parameterName, parameters[0]);
            }

            variantItem->setDescriptionToolTip(description);
            variantItem->setUserProperty(PROPERTY_ID_FUNCTION_TYPE, functionType);
            variantItem->setUserProperty(PROPERTY_ID_PARAMETER_NAME, parameterName);
            groupItem->addSubProperty(variantItem);

            ++ip_map_i;
        }
        this->addProperty(groupItem);
    }

    this->setFactoryForManager(m_variantManager, m_variantFactory);

    (void)connect(m_variantManager, &QtVariantPropertyManager::valueChanged, this,
                  &PropertyBrowserPin::pinValueChangedCallback, Qt::UniqueConnection);
    (void)connect(m_variantManager, &QtVariantPropertyManager::attributeChanged, this,
                  &PropertyBrowserPin::pinAttributeChangedCallback, Qt::UniqueConnection);

    m_pinName = name;
}

void PropertyBrowserPin::pinValueChangedCallback(const QtProperty *property, const QVariant &value) const
{
    if (m_pinName.isEmpty())
        return;

    switch (const int type = m_variantManager->propertyType(property))
    {
    case QVariant::String: {
        if (property->propertyName() == tr("Comment"))
        {
            Project.setPinComment(m_pinName, value.toString());
        }

        break;
    }
    case QVariant::Bool: {
        if (property->propertyName() == tr("Locked"))
        {
            Project.setPinLocked(m_pinName, value.toBool());
        }

        break;
    }
    case QVariant::Int: {
        break;
    }
    default: {
        if (type == QtVariantPropertyManager::enumTypeId())
        {
            const QString property_name = property->propertyName();
            const QString function_type = property->getUserProperty(PROPERTY_ID_FUNCTION_TYPE).toString();
            const QString parameter_name = property->getUserProperty(PROPERTY_ID_PARAMETER_NAME).toString();
            const QString parameter_value_translations = property->valueText();
            const QMap<QString, QString> total = Repo.getMaps(Project.hal())[function_type].ReverseTotal;
            const auto parameter_value = total[property->valueText()];

            Q_UNUSED(property_name)
            Q_UNUSED(parameter_value_translations)

            Project.setPinConfigFunctionProperty(m_pinName, function_type, parameter_name, parameter_value);
        }
        else
        {
            qDebug() << m_variantManager->propertyType(property) << property << property->propertyName() << value;
        }
        break;
    }
    }
}

void PropertyBrowserPin::pinAttributeChangedCallback(const QtProperty *property, const QString &attribute,
                                                     const QVariant &value) const
{
    Q_UNUSED(property)
    Q_UNUSED(attribute)
    Q_UNUSED(value)
}
