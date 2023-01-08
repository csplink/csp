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
// @file        MCUModule.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

global using ip_t =
    System.Collections.Generic.Dictionary<string, System.Collections.Generic.Dictionary<string, string[]>>;
using CSP.Modules.Pages.MCU.Views;
using CSP.Modules.Pages.MCU.Views.Components.Config;
using CSP.Modules.Pages.MCU.Views.Windows;
using CSP.Utils;
using Prism.Ioc;
using Prism.Modularity;
using Prism.Regions;

namespace CSP.Modules.Pages.MCU;

public class MCUModule : IModule
{
    public void OnInitialized(IContainerProvider containerProvider) {
        IRegionManager regionManager = containerProvider.Resolve<IRegionManager>();

        RegionUtil.RegisterViewWithRegion(regionManager, "Region.Window.Document", typeof(PropertyTableView));
    }

    public void RegisterTypes(IContainerRegistry containerRegistry) {
        RegionUtil.RegisterForNavigation<ConfigView>(containerRegistry, "Page.MCU.Config");
        RegionUtil.RegisterForNavigation<GPIOView>(containerRegistry, "Page.MCU.Config.PropertyTableView.GPIO");
        RegionUtil.RegisterForNavigation<ClockView>(containerRegistry, "Page.MCU.Config.PropertyTableView.Clock");
    }
}