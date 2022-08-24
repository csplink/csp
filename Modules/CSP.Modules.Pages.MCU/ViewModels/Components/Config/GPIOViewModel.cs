using CSP.Database;
using CSP.Database.Models.MCU;
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
            return true;
        }

        public void OnNavigatedFrom(NavigationContext navigationContext) {
        }

        public void OnNavigatedTo(NavigationContext navigationContext) {
        }

        #endregion INavigationAware

        private readonly IEventAggregator _eventAggregator;
        private ObservableCollection<MCUModel.PinModel.DataContextModel> _gpioCollection = new();
        private MCUModel.PinModel.DataContextModel _selectedItem;

        public GPIOViewModel(IEventAggregator eventAggregator) {
            _eventAggregator = eventAggregator;

            MCUModel mcu = MCUHelper.MCU;
            if (mcu == null)
                return;

            foreach (var pin in mcu.Pins) {
                pin.BaseProperty.PropertyChanged += OnGPIOPropertyChanged;
                if (pin.BaseProperty.IsLocked) {
                    GPIOCollection.Add(pin.BaseProperty);
                }
            }
        }

        public ObservableCollection<MCUModel.PinModel.DataContextModel> GPIOCollection {
            get => _gpioCollection;
            set => SetProperty(ref _gpioCollection, value);
        }

        public MCUModel.PinModel.DataContextModel SelectedItem {
            get => _selectedItem;
            set {
                SetProperty(ref _selectedItem, value);

                if (value == null)
                    return;

                if (value.Position - 1 < MCUHelper.MCU.Pins.Length) {
                    //  _eventAggregator.GetEvent<PropertyEvent>().Publish(MCUHelper.MCU.Pins[value.Position - 1].GPIOProperty);
                }
            }
        }

        private void OnGPIOPropertyChanged(object sender, PropertyChangedEventArgs e) {
            if (e.PropertyName != "IsLocked")
                return;

            if (sender is MCUModel.PinModel.DataContextModel value) {
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