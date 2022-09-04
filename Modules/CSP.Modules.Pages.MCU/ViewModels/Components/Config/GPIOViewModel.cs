using CSP.Events;
using CSP.Modules.Pages.MCU.Models;
using CSP.Modules.Pages.MCU.Tools;
using Prism.Events;
using Prism.Mvvm;
using Prism.Regions;
using System.Collections.ObjectModel;
using System.ComponentModel;

namespace CSP.Modules.Pages.MCU.ViewModels.Components.Config
{
    public class GPIOViewModel : BindableBase, INavigationAware
    {
        #region INavigationAware

        public bool IsNavigationTarget(NavigationContext navigationContext) {
            return false;
        }

        public void OnNavigatedFrom(NavigationContext navigationContext) {
        }

        public void OnNavigatedTo(NavigationContext navigationContext) {
        }

        #endregion INavigationAware

        private readonly IEventAggregator _eventAggregator;
        private ObservableCollection<PinModel> _gpioCollection = new();
        private PinModel _selectedItem;

        public GPIOViewModel(IEventAggregator eventAggregator) {
            _eventAggregator = eventAggregator;

            if (DescriptionHelper.Pinout == null)
                return;

            foreach (var pin in DescriptionHelper.Pinout.Pins) {
                var property = DescriptionHelper.GetPinProperty(pin.Name);
                property.PropertyChanged += OnGPIOPropertyChanged;
                if (property.IsLocked) {
                    GPIOCollection.Add(property);
                }
            }
        }

        public ObservableCollection<PinModel> GPIOCollection {
            get => _gpioCollection;
            set => SetProperty(ref _gpioCollection, value);
        }

        public PinModel SelectedItem {
            get => _selectedItem;
            set {
                SetProperty(ref _selectedItem, value);

                if (value == null)
                    return;

                _eventAggregator.GetEvent<PropertyEvent>().Publish(value.Property);
            }
        }

        private void OnGPIOPropertyChanged(object sender, PropertyChangedEventArgs e) {
            if (e.PropertyName != "IsLocked")
                return;

            if (sender is PinModel value) {
                if (value.IsLocked) {
                    GPIOCollection.Add(value);
                }
                else {
                    GPIOCollection.Remove(value);
                }
            }
        }
    }
}