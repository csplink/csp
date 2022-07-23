using CSP.Modules.Dialogs.NewMCU.ViewModels;
using CSP.Modules.Dialogs.NewMCU.Views;
using CSP.Utils;
using Prism.Ioc;
using Prism.Modularity;

namespace CSP.Modules.Dialogs.NewMCU
{
    public class NewMCUModule : IModule
    {
        public void OnInitialized(IContainerProvider containerProvider)
        {
        }

        public void RegisterTypes(IContainerRegistry containerRegistry)
        {
            DialogUtil.RegisterDialog<MCUSelectorView, MCUSelectorViewModel>(containerRegistry, "Dialog.NewMCU");
        }
    }
}