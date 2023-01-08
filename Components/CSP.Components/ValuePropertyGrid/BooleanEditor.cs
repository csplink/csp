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
// @file        BooleanEditor.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System.ComponentModel;
using System.Reflection;
using System.Windows.Controls;
using System.Windows.Data;
using Prism.Mvvm;
using Syncfusion.Windows.PropertyGrid;

namespace CSP.Components.ValuePropertyGrid;

public class BooleanEditor : BaseTypeEditor
{
    private CheckBox _checkBox;

    public override void Attach(PropertyViewItem property, PropertyItem info) {
        if (info.Value is not BooleanEditorModel) {
            return;
        }

        Binding binding = new Binding("Value.Boolean") {
            Mode                = BindingMode.TwoWay,
            Source              = info,
            UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
        };
        BindingOperations.SetBinding(_checkBox, CheckBox.IsCheckedProperty, binding);

        binding = new Binding("Value.Boolean") {
            Mode                = BindingMode.TwoWay,
            Source              = info,
            UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
        };
        BindingOperations.SetBinding(_checkBox, CheckBox.ToolTipProperty, binding);

        _checkBox.IsEnabled = !info.IsReadOnly;
    }

    public override object Create(PropertyInfo propertyInfo) {
        return CreateEditor();
    }

    public override object Create(PropertyDescriptor propertyDescriptor) {
        return CreateEditor();
    }

    public override void Detach(PropertyViewItem property) {
        _checkBox = null;
    }

    private CheckBox CreateEditor() {
        _checkBox = new CheckBox();

        return _checkBox;
    }
}

public class BooleanEditorModel : BindableBase
{
    private bool _boolean;

    public bool Boolean {
        get => _boolean;
        set => SetProperty(ref _boolean, value);
    }
}