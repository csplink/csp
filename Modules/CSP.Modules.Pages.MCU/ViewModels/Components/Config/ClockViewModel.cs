using CSP.Events;
using CSP.Modules.Pages.MCU.Tools;
using Prism.Events;
using Prism.Mvvm;
using Prism.Regions;

namespace CSP.Modules.Pages.MCU.ViewModels.Components.Config
{
    public class ClockViewModel : BindableBase, INavigationAware
    {
        #region INavigationAware

        public bool IsNavigationTarget(NavigationContext navigationContext) {
            return false;
        }

        public void OnNavigatedFrom(NavigationContext navigationContext) {
        }

        public void OnNavigatedTo(NavigationContext navigationContext) {
            _eventAggregator.GetEvent<PropertyEvent>().Publish(null);
            if (DescriptionHelper.Properties.ContainsKey("Clock"))
                _eventAggregator.GetEvent<PropertyEvent>().Publish(DescriptionHelper.Properties["Clock"]);
        }

        #endregion INavigationAware

        private readonly IEventAggregator _eventAggregator;

        public ClockViewModel(IEventAggregator eventAggregator) {
            _eventAggregator = eventAggregator;

            if (!DescriptionHelper.Properties.ContainsKey("Clock")) {
                DescriptionHelper.Properties.Add("Clock", DescriptionHelper.CreateClockPropertyDetails());
            }
        }
    }
}