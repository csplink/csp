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
// @file        PropertyView.xaml.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using CSP.Events;
using Prism.Events;
using Prism.Ioc;
using Syncfusion.Windows.PropertyGrid;

namespace CSP.Apps.Dev.Views.Windows;

public partial class PropertyView
{
    public PropertyView() {
        InitializeComponent();

        IContainerExtension containerExtension = ContainerLocator.Current;
        IEventAggregator    eventAggregator    = containerExtension.Resolve<IEventAggregator>();
        eventAggregator.GetEvent<PropertyEvent>().Subscribe(OnPropertyReceive);
        eventAggregator.GetEvent<CustomEditorEvent>().Subscribe(OnCustomEditorReceive);
    }

    private void OnCustomEditorReceive(CustomEditor editor) {
        Property.CustomEditorCollection.Add(editor);
    }

    private void OnPropertyReceive(object property) {
        Property.SelectedObject = property;
    }
}