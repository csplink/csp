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
// @file        DockControl.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System.Windows;
using System.Windows.Controls;

namespace CSP.Components;

public class DockControl : UserControl
{
    public static readonly DependencyProperty IconProperty = DependencyProperty.Register("Icon",
        typeof(Image),
        typeof(DockControl),
        new FrameworkPropertyMetadata(null, OnIconChanged) { BindsTwoWayByDefault = true });

    public static readonly DependencyProperty KeyProperty = DependencyProperty.Register("Key",
        typeof(char),
        typeof(DockControl),
        new FrameworkPropertyMetadata('a', OnKeyChanged) { BindsTwoWayByDefault = true });

    public DockControl() {
    }

    public Image Icon {
        get => (Image)GetValue(IconProperty);
        set => SetValue(IconProperty, value);
    }

    public char Key {
        get => (char)GetValue(KeyProperty);
        set => SetValue(KeyProperty, value);
    }

    private static void OnIconChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
    }

    private static void OnKeyChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
    }
}