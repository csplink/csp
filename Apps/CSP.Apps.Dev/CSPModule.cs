using CSP.Apps.Dev.Views;
using CSP.Apps.Dev.Views.Windows;
using CSP.Utils;
using Prism.Ioc;
using Prism.Modularity;
using Prism.Regions;

namespace CSP.Apps.Dev
{
    public class CSPModule : IModule
    {
        public void OnInitialized(IContainerProvider containerProvider) {
            var regionManager = containerProvider.Resolve<IRegionManager>();
            RegionUtil.RegisterViewWithRegion(regionManager, "Region.Window.Document", typeof(OutputView));
            RegionUtil.RegisterViewWithRegion(regionManager, "Region.Window.Document", typeof(SolutionExplorerView));
            RegionUtil.RegisterViewWithRegion(regionManager, "Region.Window.Document", typeof(PropertyView));
        }

        public void RegisterTypes(IContainerRegistry containerRegistry) {
            RegionUtil.RegisterForNavigation<HomeView>(containerRegistry, "Page.Home");
            DialogUtil.RegisterDialogWindow<DialogWindowView>(containerRegistry, "DialogWindow");
        }
    }
}