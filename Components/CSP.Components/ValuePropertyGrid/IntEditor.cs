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
// @file        IntEditor.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System.ComponentModel;
using System.Reflection;
using System.Windows.Data;
using Prism.Mvvm;
using Syncfusion.Windows.PropertyGrid;
using Syncfusion.Windows.Shared;

namespace CSP.Components.ValuePropertyGrid;

public class IntEditor : BaseTypeEditor
{
    private IntegerTextBox _integerTextBox;

    public override void Attach(PropertyViewItem property, PropertyItem info) {
        if (info.Value is not IntEditorModel) {
            return;
        }

        Binding binding = new Binding("Value.Boolean") {
            Mode                = BindingMode.TwoWay,
            Source              = info,
            UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
        };
        BindingOperations.SetBinding(_integerTextBox, IntegerTextBox.ValueProperty, binding);

        binding = new Binding("Value.Boolean") {
            Mode                = BindingMode.TwoWay,
            Source              = info,
            UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
        };
        BindingOperations.SetBinding(_integerTextBox, IntegerTextBox.ToolTipProperty, binding);

        _integerTextBox.IsReadOnly = info.IsReadOnly;
    }

    public override object Create(PropertyInfo propertyInfo) {
        return CreateEditor();
    }

    public override object Create(PropertyDescriptor propertyDescriptor) {
        return CreateEditor();
    }

    public override void Detach(PropertyViewItem property) {
        _integerTextBox = null;
    }

    private IntegerTextBox CreateEditor() {
        _integerTextBox = new IntegerTextBox();

        return _integerTextBox;
    }
}

public class IntEditorModel : BindableBase
{
    private int _int;

    public int Int {
        get => _int;
        set => SetProperty(ref _int, value);
    }
}