// Licensed under the Apache License, Version 2.0 (the "License");
// You may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// Copyright (C) 2022-2023 xqyjlj<xqyjlj@126.com>
//
// @author      xqyjlj
// @file        PinConfigModel.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Reflection;
using System.Xml.Serialization;
using CSP.Components.ValuePropertyGrid;
using CSP.Events;
using CSP.Utils;
using Prism.Mvvm;

namespace CSP.Models.Internal;

public class PinConfigModel : BindableBase
{
    [ReadOnly(true)]
    [Display(Name = "功能", Description = "Pin 功能", GroupName = "系统")]
    [XmlAttribute]
    public StringEditorModel Function { get; } = new();

    [ReadOnly(false)]
    [Display(Name = "锁定", Description = "锁定", GroupName = "基础")]
    [XmlAttribute]
    public BooleanEditorModel IsLocked { get; } = new();

    [ReadOnly(false)]
    [Display(Name = "标签", Description = "Pin 标签, 用于宏定义", GroupName = "基础")]
    [XmlAttribute]
    public StringEditorModel Label { get; } = new();

    [ReadOnly(true)]
    [Display(Name = "名称", Description = "Pin 名称", GroupName = "基础")]
    [XmlAttribute]
    public StringEditorModel Name { get; } = new();

    [ReadOnly(true)]
    [Display(Name = "引脚序号", Description = "Pin 引脚序号", GroupName = "基础")]
    [XmlAttribute]
    public StringEditorModel Position { get; } = new();

    public PropertyDetails Property { get; } = new();

    public ObservableDictionary<string, ObservableDictionary<string, Attribute>> GetAttributes() {
        ObservableDictionary<string, ObservableDictionary<string, Attribute>> rtn = new();
        PropertyInfo[] infos = typeof(PinConfigModel).GetProperties();
        foreach (PropertyInfo info in infos) {
            object[] attrs = info.GetCustomAttributes(false);
            if (attrs.Length > 0) {
                ObservableDictionary<string, Attribute> attributes = new();
                foreach (object attr in attrs) {
                    switch (attr) {
                    case DisplayAttribute displayAttribute: {
                        if (displayAttribute.Name != null) {
                            attributes.Add("DisplayName", new DisplayNameAttribute(displayAttribute.Name));
                        }

                        if (displayAttribute.Description != null) {
                            attributes.Add("Description", new DescriptionAttribute(displayAttribute.Description));
                        }

                        if (displayAttribute.GroupName != null) {
                            attributes.Add("Category", new CategoryAttribute(displayAttribute.GroupName));
                        }

                        break;
                    }
                    case ReadOnlyAttribute readOnlyAttribute: {
                        attributes.Add("ReadOnly", new ReadOnlyAttribute(readOnlyAttribute.IsReadOnly));

                        break;
                    }
                    }
                }

                rtn.Add(info.Name, attributes);
            }
        }

        return rtn;
    }

    public ObservableDictionary<string, object> GetDetails() {
        ObservableDictionary<string, object> rtn = new() {
            { "Function", Function },
            { "IsLocked", IsLocked },
            { "Label", Label },
            { "Name", Name },
            { "Position", Position }
        };

        return rtn;
    }
}