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
// @file        RegionUtil.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System;
using System.Collections.Generic;
using System.Linq;
using Prism.Ioc;
using Prism.Regions;

namespace CSP.Utils;

public static class RegionUtil
{
    private static readonly List<string> Names = new();

    public static IEnumerable<string> Views => Names;

    public static void RegisterForNavigation<T>(IContainerRegistry containerRegistry, string viewName) {
        containerRegistry.RegisterForNavigation<T>(viewName);

        AddView(viewName);
    }

    public static void RegisterViewWithRegion(IRegionManager regionManager, string regionName, Type viewType) {
        regionManager.RegisterViewWithRegion(regionName, viewType);
    }

    public static void RequestNavigate(IRegionManager regionManager, string regionName, string viewName) {
        if (regionManager.Regions.ContainsRegionWithName(regionName) && Views.Contains(viewName)) {
            regionManager.RequestNavigate(regionName, viewName);
        }
    }

    public static void RequestNavigate(IRegionManager regionManager, string regionName, string viewName,
        NavigationParameters                          navigationParameters) {
        if (regionManager.Regions.ContainsRegionWithName(regionName) && Views.Contains(viewName)) {
            regionManager.RequestNavigate(regionName, viewName, navigationParameters);
        }
    }

    private static void AddView(string name) {
        Names.Add(name);
    }
}