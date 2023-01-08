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
// @file        StringEditor.cs
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

public class StringEditor : BaseTypeEditor
{
    private TextBox _textBox;

    public override void Attach(PropertyViewItem property, PropertyItem info) {
        if (info.Value is not StringEditorModel) {
            return;
        }

        Binding binding = new Binding("Value.String") {
            Mode                = BindingMode.TwoWay,
            Source              = info,
            UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
        };
        BindingOperations.SetBinding(_textBox, TextBox.TextProperty, binding);

        binding = new Binding("Value.String") {
            Mode                = BindingMode.TwoWay,
            Source              = info,
            UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
        };
        BindingOperations.SetBinding(_textBox, TextBox.ToolTipProperty, binding);

        _textBox.IsReadOnly = info.IsReadOnly;
    }

    public override object Create(PropertyInfo propertyInfo) {
        return CreateEditor();
    }

    public override object Create(PropertyDescriptor propertyDescriptor) {
        return CreateEditor();
    }

    public override void Detach(PropertyViewItem property) {
        _textBox = null;
    }

    private TextBox CreateEditor() {
        _textBox = new TextBox();

        return _textBox;
    }
}

public class StringEditorModel : BindableBase
{
    private string _string = string.Empty;

    public string String {
        get => _string;
        set => SetProperty(ref _string, value);
    }
}