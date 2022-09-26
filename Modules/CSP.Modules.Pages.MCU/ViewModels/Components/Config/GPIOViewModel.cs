using CSP.Events;
using CSP.Modules.Pages.MCU.Models;
using CSP.Modules.Pages.MCU.Tools;
using CSP.Resources;
using Microsoft.Xaml.Behaviors;
using Prism.Events;
using Prism.Mvvm;
using Prism.Regions;
using Syncfusion.UI.Xaml.TreeView;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Windows.Data;

namespace CSP.Modules.Pages.MCU.ViewModels.Components.Config
{
    public class GPIOViewModel : BindableBase, INavigationAware
    {
        #region INavigationAware

        public bool IsNavigationTarget(NavigationContext navigationContext) {
            return false;
        }

        public void OnNavigatedFrom(NavigationContext navigationContext) {
            foreach (var pin in DescriptionHelper.Pinout.Pins) {
                var property = DescriptionHelper.GetPinProperty(pin.Name);
                property.PropertyChanged -= OnGPIOPropertyChanged;
            }
        }

        public void OnNavigatedTo(NavigationContext navigationContext) {
        }

        #endregion INavigationAware

        internal FilterChangedDelegate FilterChanged;
        private readonly IEventAggregator _eventAggregator;
        private string _filterText = string.Empty;
        private ObservableCollection<SolutionExplorerEvent.Model> _gpioCollection = new();
        private PinModel _selectedItem;

        public GPIOViewModel(IEventAggregator eventAggregator) {
            _eventAggregator = eventAggregator;

            if (DescriptionHelper.Pinout == null)
                return;

            foreach (var pin in DescriptionHelper.Pinout.Pins) {
                var property = DescriptionHelper.GetPinProperty(pin.Name);
                property.PropertyChanged += OnGPIOPropertyChanged;
                if (property.IsLocked.Boolean) {
                    GPIOCollection.Add(new SolutionExplorerEvent.Model { Name = property.Name.String, Image = Icon.Pin });
                }
            }

            CollectionView = new ListCollectionView(GPIOCollection);
        }

        internal delegate void FilterChangedDelegate();

        public ListCollectionView CollectionView { get; }

        public string FilterText {
            get => _filterText;
            set {
                if (SetProperty(ref _filterText, value)) {
                    FilterChanged?.Invoke();
                }
            }
        }

        public ObservableCollection<SolutionExplorerEvent.Model> GPIOCollection {
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
                if (value.IsLocked.Boolean) {
                    GPIOCollection.Add(new SolutionExplorerEvent.Model { Name = value.Name.String, Image = Icon.Pin });
                }
                else {
                    SolutionExplorerEvent.Model model = null;
                    foreach (var gpio in GPIOCollection) {
                        if (gpio.Name == value.Name.String) {
                            model = gpio;
                            break;
                        }
                    }
                    GPIOCollection.Remove(model);
                }
            }
        }
    }

    public class TreeViewFilterTrigger : TargetedTriggerAction<SfTreeView>
    {
        protected override void Invoke(object parameter) {
            if (this.Target.DataContext is GPIOViewModel viewModel)
                viewModel.FilterChanged += OnFilterChanged;
        }

        private void OnFilterChanged() {
            if (this.Target.DataContext is not GPIOViewModel viewModel)
                return;

            viewModel.CollectionView.Filter = e => {
                if (e is SolutionExplorerEvent.Model model) {
                    if (model.Name.ToLower().Contains(viewModel.FilterText.ToLower()))
                        return true;
                    if (model.Children != null) {
                        foreach (var child in model.Children)
                            if (child.Name.ToLower().Contains(viewModel.FilterText.ToLower()))
                                return true;
                    }
                }
                return false;
            };
            this.Target.ExpandAll();
        }
    }
}