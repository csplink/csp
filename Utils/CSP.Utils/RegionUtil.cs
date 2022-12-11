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