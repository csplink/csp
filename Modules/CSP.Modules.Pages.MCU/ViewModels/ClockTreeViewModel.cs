using Prism.Events;
using Prism.Mvvm;
using Prism.Regions;

namespace CSP.Modules.Pages.MCU.ViewModels
{
    public class ClockTreeViewModel : BindableBase
    {
        private readonly IEventAggregator _eventAggregator;
        private readonly IRegionManager _regionManager;

        public ClockTreeViewModel(IRegionManager regionManager, IEventAggregator eventAggregator) {
            _regionManager = regionManager;
            _eventAggregator = eventAggregator;
        }
    }
}