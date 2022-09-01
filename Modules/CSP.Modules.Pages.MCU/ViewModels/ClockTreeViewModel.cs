using CSP.Modules.Pages.MCU.Tools;
using CSP.Resources;
using Prism.Events;
using Prism.Mvvm;
using Prism.Regions;
using System;

namespace CSP.Modules.Pages.MCU.ViewModels
{
    public class ClockTreeViewModel : BindableBase
    {
        private readonly IEventAggregator _eventAggregator;
        private readonly IRegionManager _regionManager;
        private Uri _clockTreeImage;

        public ClockTreeViewModel(IRegionManager regionManager, IEventAggregator eventAggregator) {
            _regionManager = regionManager;
            _eventAggregator = eventAggregator;

            ClockTreeImage = new Uri($"{DescriptionHelper.RepositoryPath}/description/{DescriptionHelper.Name.ToLower()}/clock/{DescriptionHelper.MCU.Name}.svg");
        }

        public Uri ClockTreeImage {
            get => _clockTreeImage;
            set => SetProperty(ref _clockTreeImage, value);
        }
    }
}