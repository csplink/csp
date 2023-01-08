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
// @file        RegionAdapter.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System.Collections.Specialized;
using System.Windows;
using Prism.Regions;

namespace CSP.Apps.Dev.RegionAdapter.DockingManager;

public class RegionAdapter : RegionAdapterBase<Syncfusion.Windows.Tools.Controls.DockingManager>
{
    public RegionAdapter(IRegionBehaviorFactory regionBehaviorFactory) : base(regionBehaviorFactory) {
    }

    protected override void Adapt(IRegion region, Syncfusion.Windows.Tools.Controls.DockingManager regionTarget) {
        region.Views.CollectionChanged += (_, e) => {
            if (e.Action == NotifyCollectionChangedAction.Add) {
                if (e.NewItems != null) {
                    foreach (FrameworkElement element in e.NewItems) {
                        if (!regionTarget.Children.Contains(element)) {
                            regionTarget.BeginInit();
                            regionTarget.Children.Add(element);
                            regionTarget.EndInit();
                        }
                    }
                }
            }
        };
    }

    protected override void AttachBehaviors(IRegion      region,
        Syncfusion.Windows.Tools.Controls.DockingManager regionTarget) {
        base.AttachBehaviors(region, regionTarget);
        if (!region.Behaviors.ContainsKey(DocumentRegionActiveAwareBehavior.BehaviorKey)) {
            region.Behaviors.Add(DocumentRegionActiveAwareBehavior.BehaviorKey,
                new DocumentRegionActiveAwareBehavior { HostControl = regionTarget });
        }
    }

    protected override IRegion CreateRegion() {
        return new SingleActiveRegion();
    }
}