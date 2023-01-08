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
// @file        Pin.xaml.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System.Windows;
using CSP.Modules.Pages.MCU.Enums;

namespace CSP.Modules.Pages.MCU.Components.LQFP;

public partial class Pin
{
    public static readonly DependencyProperty DirectionProperty = DependencyProperty.Register("Direction",
        typeof(DirectionEnum),
        typeof(Pin),
        new FrameworkPropertyMetadata(DirectionEnum.Top, OnDirectionChanged) { BindsTwoWayByDefault = true });

    public Pin() {
        InitializeComponent();
    }

    public DirectionEnum Direction {
        get => (DirectionEnum)GetValue(DirectionProperty);
        set => SetValue(DirectionProperty, value);
    }

    private static void OnDirectionChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        if (d is not Pin pin) {
            return;
        }

        if (e.NewValue is not DirectionEnum direction) {
            return;
        }

        pin.ContentTemplate = pin.Resources[$"Pin{direction.ToString()}"] as DataTemplate;
    }
}