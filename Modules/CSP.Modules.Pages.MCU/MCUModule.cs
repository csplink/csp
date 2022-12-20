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