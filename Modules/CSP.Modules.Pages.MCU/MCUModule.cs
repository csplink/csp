using CSP.Modules.Pages.MCU.Views;
using CSP.Modules.Pages.MCU.Views.Components.Config;
using CSP.Modules.Pages.MCU.Views.Components.Package;
using CSP.Modules.Pages.MCU.Views.Windows;
using CSP.Utils;
using Prism.Ioc;
using Prism.Modularity;
using Prism.Regions;

namespace CSP.Modules.Pages.MCU
{
    public class MCUModule : IModule
    {
        public void OnInitialized(IContainerProvider containerProvider) {
            var regionManager = containerProvider.Resolve<IRegionManager>();

            RegionUtil.RegisterViewWithRegion(regionManager, "Region.Window.Document", typeof(MCUConfigView));
        }

        public void RegisterTypes(IContainerRegistry containerRegistry) {
            RegionUtil.RegisterForNavigation<PinConfigView>(containerRegistry, "Page.MCU.PinConfig");
            RegionUtil.RegisterForNavigation<GPIOView>(containerRegistry, "Page.MCU.PinConfig.MCUConfig.GPIO");
            RegionUtil.RegisterForNavigation<LQFP48View>(containerRegistry, "Page.MCU.Package.LQFP48");
            RegionUtil.RegisterForNavigation<LQFP64View>(containerRegistry, "Page.MCU.Package.LQFP64");
            RegionUtil.RegisterForNavigation<LQFP144View>(containerRegistry, "Page.MCU.Package.LQFP144");
        }
    }
}