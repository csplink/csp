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
// @file        DocumentRegionActiveAwareBehavior .cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System.Windows;
using System.Windows.Controls;
using Prism.Regions;
using Prism.Regions.Behaviors;
using Syncfusion.Windows.Tools.Controls;

namespace CSP.Apps.Dev.RegionAdapter.DockingManager;

public class DocumentRegionActiveAwareBehavior : RegionBehavior, IHostAwareRegionBehavior
{
    public const string           BehaviorKey = "DocumentRegionActiveAwareBehavior";
    private      DependencyObject _hostControl;

    public DependencyObject HostControl {
        get => _hostControl;
        set => _hostControl = value as Syncfusion.Windows.Tools.Controls.DockingManager;
    }

    protected override void OnAttach() {
        if (HostControl is Syncfusion.Windows.Tools.Controls.DockingManager {
                DocContainer: DocumentContainer docContainer
            }) {
            docContainer.AddTabDocumentAtLast  =  true;
            docContainer.ActiveDocumentChanged += DocumentRegionActiveAwareBehavior_ActiveDocumentChanged;
        }
    }

    private void DocumentRegionActiveAwareBehavior_ActiveDocumentChanged(DependencyObject d,
        DependencyPropertyChangedEventArgs                                                e) {
        if (e.OldValue != null) {
            object item = e.OldValue;

            //are we dealing with a ContentPane directly
            if (Region.Views.Contains(item) && Region.ActiveViews.Contains(item)) {
                Region.Deactivate(item);
            }
            else {
                //now check to see if we have any views that were injected
                if (item is ContentControl contentControl) {
                    object injectedView = contentControl.Content;
                    if (Region.Views.Contains(injectedView) && Region.ActiveViews.Contains(injectedView)) {
                        Region.Deactivate(injectedView);
                    }
                }
            }
        }

        if (e.NewValue != null) {
            object item = e.NewValue;

            //are we dealing with a ContentPane directly
            if (Region.Views.Contains(item) && !Region.ActiveViews.Contains(item)) {
                Region.Activate(item);
            }
            else {
                //now check to see if we have any views that were injected
                if (item is ContentControl contentControl) {
                    object injectedView = contentControl.Content;
                    if (Region.Views.Contains(injectedView) && !Region.ActiveViews.Contains(injectedView)) {
                        Region.Activate(injectedView);
                    }
                }
            }
        }
    }
}