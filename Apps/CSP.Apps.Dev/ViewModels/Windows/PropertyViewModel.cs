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
// @file        PropertyViewModel.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using CSP.Components.ValuePropertyGrid;
using CSP.Events;
using Prism.Events;
using Prism.Mvvm;
using Syncfusion.Windows.PropertyGrid;

namespace CSP.Apps.Dev.ViewModels.Windows;

public class PropertyViewModel : BindableBase
{
    private readonly IEventAggregator _eventAggregator;

    public PropertyViewModel(IEventAggregator eventAggregator) {
        _eventAggregator = eventAggregator;

        eventAggregator.GetEvent<RenderedEvent>().Subscribe(name => { AddCustomEditor(); });
    }

    private void AddCustomEditor() {
        CustomEditor editor = new() {
            Editor          = new DictionaryEditor(),
            HasPropertyType = true,
            PropertyType    = typeof(DictionaryEditorModel)
        };
        _eventAggregator.GetEvent<CustomEditorEvent>().Publish(editor);

        editor = new CustomEditor {
            Editor          = new StringEditor(),
            HasPropertyType = true,
            PropertyType    = typeof(StringEditorModel)
        };
        _eventAggregator.GetEvent<CustomEditorEvent>().Publish(editor);

        editor = new CustomEditor {
            Editor          = new BooleanEditor(),
            HasPropertyType = true,
            PropertyType    = typeof(BooleanEditorModel)
        };
        _eventAggregator.GetEvent<CustomEditorEvent>().Publish(editor);

        editor = new CustomEditor {
            Editor          = new IntEditor(),
            HasPropertyType = true,
            PropertyType    = typeof(IntEditorModel)
        };
        _eventAggregator.GetEvent<CustomEditorEvent>().Publish(editor);
    }
}