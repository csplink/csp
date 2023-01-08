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
// @file        MCUSelectorView.xaml.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using CSP.Modules.Dialogs.NewMCU.Models;
using CSP.Utils;
using Syncfusion.UI.Xaml.TreeView;

namespace CSP.Modules.Dialogs.NewMCU.Views;

public partial class MCUSelectorView
{
    public MCUSelectorView() {
        InitializeComponent();
    }

    private void OnSelectionChanged(object sender, ItemSelectionChangedEventArgs e) {
        object item = TreeView.SelectedItem;

        if (item is not DocumentModel value) {
            return;
        }

        if (!string.IsNullOrWhiteSpace(value.Url)) {
            Util.OpenUrl(value.Url);
        }
    }
}