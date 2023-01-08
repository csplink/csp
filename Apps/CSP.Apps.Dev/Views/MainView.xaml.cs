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
// @file        MainView.xaml.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System.Globalization;
using System.Threading;
using CSP.Utils;

namespace CSP.Apps.Dev.Views;

public partial class MainView
{
    public MainView() {
        Thread.CurrentThread.CurrentUICulture = new CultureInfo("zh-Hans");
        ThemesUtil.SetThemes(this, "Office2019Colorful");
        InitializeComponent();
    }

    // private void OnDockingManagerMainChildrenCollectionChanged(object sender, NotifyCollectionChangedEventArgs e)
    // {
    //     MenuView.Items.Clear();
    //     MenuView.Items.Add(new MenuItem { Header = "打开方式(_N)" });
    //     MenuView.Items.Add(new Separator());
    //     foreach (var child in DockingManagerMain.Children)
    //     {
    //         if (child is not DockControlModel dock)
    //             return;
    //
    //         var headerObj = DockingManager.GetHeader(dock);
    //
    //         if (headerObj is not string header)
    //             return;
    //
    //         if (dock.Key >= 'A' && dock.Key <= 'Z')
    //         {
    //             header = $"{header}(_{dock.Key})";
    //         }
    //
    //         MenuView.Items.Add(new MenuItem { Header = header, Icon = dock.Icon });
    //     }
    // }
}