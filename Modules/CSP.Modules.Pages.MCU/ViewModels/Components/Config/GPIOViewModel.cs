using Prism.Events;
using Prism.Mvvm;
using Prism.Regions;

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
        // private ObservableCollection<PinoutModel.PinModel.DataContextModel> _gpioCollection = new();
        // private PinoutModel.PinModel.DataContextModel _selectedItem;

        public GPIOViewModel(IEventAggregator eventAggregator) {
            _eventAggregator = eventAggregator;

            // PinoutModel mcu = MCUHelper.MCU;
            // if (mcu == null)
            //     return;
            //
            // foreach (var pin in mcu.Pins) {
            //     pin.BaseProperty.PropertyChanged += OnGPIOPropertyChanged;
            //     if (pin.BaseProperty.IsLocked) {
            //         GPIOCollection.Add(pin.BaseProperty);
            //     }
            // }
        }

        // public ObservableCollection<PinoutModel.PinModel.DataContextModel> GPIOCollection {
        //     get => _gpioCollection;
        //     set => SetProperty(ref _gpioCollection, value);
        // }
        //
        // public PinoutModel.PinModel.DataContextModel SelectedItem {
        //     get => _selectedItem;
        //     set {
        //         SetProperty(ref _selectedItem, value);
        //
        //         if (value == null)
        //             return;
        //
        //         if (value.Position - 1 < MCUHelper.MCU.Pins.Length) {
        //             //  _eventAggregator.GetEvent<PropertyEvent>().Publish(MCUHelper.MCU.Pins[value.Position - 1].GPIOProperty);
        //         }
        //     }
        // }
        //
        // private void OnGPIOPropertyChanged(object sender, PropertyChangedEventArgs e) {
        //     if (e.PropertyName != "IsLocked")
        //         return;
        //
        //     if (sender is PinoutModel.PinModel.DataContextModel value) {
        //         if (value.IsLocked) {
        //             GPIOCollection.Add(value);
        //         }
        //         else {
        //             GPIOCollection.Remove(value);
        //         }
        //     }
        // }
    }
}