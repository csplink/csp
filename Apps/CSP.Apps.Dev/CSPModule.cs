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
// @file        CSPModule.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using CSP.Apps.Dev.Views;
using CSP.Apps.Dev.Views.Windows;
using CSP.Utils;
using Prism.Ioc;
using Prism.Modularity;
using Prism.Regions;

namespace CSP.Apps.Dev;

public class CSPModule : IModule
{
    public void OnInitialized(IContainerProvider containerProvider) {
        IRegionManager regionManager = containerProvider.Resolve<IRegionManager>();
        RegionUtil.RegisterViewWithRegion(regionManager, "Region.Window.Document", typeof(OutputView));
        RegionUtil.RegisterViewWithRegion(regionManager, "Region.Window.Document", typeof(SolutionExplorerView));
        RegionUtil.RegisterViewWithRegion(regionManager, "Region.Window.Document", typeof(PropertyView));
    }

    public void RegisterTypes(IContainerRegistry containerRegistry) {
        RegionUtil.RegisterForNavigation<HomeView>(containerRegistry, "Page.Home");
        DialogUtil.RegisterDialogWindow<DialogWindowView>(containerRegistry, "DialogWindow");
    }
}