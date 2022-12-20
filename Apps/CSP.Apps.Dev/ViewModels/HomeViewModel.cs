using Prism.Mvvm;
using Prism.Regions;

namespace CSP.Apps.Dev.ViewModels;

public class HomeViewModel : BindableBase, INavigationAware
{
    #region INavigationAware

    public bool IsNavigationTarget(NavigationContext navigationContext) {
        return true;
    }

    public void OnNavigatedFrom(NavigationContext navigationContext) {
    }

    public void OnNavigatedTo(NavigationContext navigationContext) {
    }

    #endregion INavigationAware
}