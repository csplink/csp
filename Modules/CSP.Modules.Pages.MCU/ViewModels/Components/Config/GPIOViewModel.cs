using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Windows.Data;
using CSP.Events;
using CSP.Models.Internal;
using CSP.Resources;
using CSP.Singleton.Internal;
using Microsoft.Xaml.Behaviors;
using Prism.Events;
using Prism.Mvvm;
using Prism.Regions;
using Syncfusion.UI.Xaml.TreeView;

namespace CSP.Modules.Pages.MCU.ViewModels.Components.Config;

public class GPIOViewModel : BindableBase, INavigationAware
{
    private readonly IEventAggregator                                  _eventAggregator;
    private          string                                            _filterText     = string.Empty;
    private          ObservableCollection<SolutionExplorerEvent.Model> _gpioCollection = new();
    private          PinConfigModel                                    _selectedItem;

    internal FilterChangedDelegate FilterChanged;

    public GPIOViewModel(IEventAggregator eventAggregator) {
        _eventAggregator = eventAggregator;

        if (PinConfigSingleton.PinConfigs == null) {
            return;
        }

        foreach (var (_, pin) in PinConfigSingleton.PinConfigs) {
            pin.PropertyChanged += OnGPIOPropertyChanged;
            if (pin.IsLocked.Boolean) {
                GPIOCollection.Add(new SolutionExplorerEvent.Model { Name = pin.Name.String, Image = Icon.Pin });
            }
        }

        CollectionView = new ListCollectionView(GPIOCollection);
    }

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

    public PinConfigModel SelectedItem {
        get => _selectedItem;
        set {
            SetProperty(ref _selectedItem, value);

            if (value == null) {
                return;
            }

            _eventAggregator.GetEvent<PropertyEvent>().Publish(value.Property);
        }
    }

    private void OnGPIOPropertyChanged(object sender, PropertyChangedEventArgs e) {
        if (e.PropertyName != "IsLocked") {
            return;
        }

        if (sender is PinConfigModel value) {
            if (value.IsLocked.Boolean) {
                GPIOCollection.Add(new SolutionExplorerEvent.Model { Name = value.Name.String, Image = Icon.Pin });
            }
            else {
                SolutionExplorerEvent.Model model = null;
                foreach (SolutionExplorerEvent.Model gpio in GPIOCollection) {
                    if (gpio.Name == value.Name.String) {
                        model = gpio;

                        break;
                    }
                }

                GPIOCollection.Remove(model);
            }
        }
    }

    internal delegate void FilterChangedDelegate();

    #region INavigationAware

    public bool IsNavigationTarget(NavigationContext navigationContext) {
        return false;
    }

    public void OnNavigatedFrom(NavigationContext navigationContext) {
        foreach (var (_, pin) in PinConfigSingleton.PinConfigs) {
            pin.PropertyChanged -= OnGPIOPropertyChanged;
        }
    }

    public void OnNavigatedTo(NavigationContext navigationContext) {
    }

    #endregion INavigationAware
}

public class TreeViewFilterTrigger : TargetedTriggerAction<SfTreeView>
{
    protected override void Invoke(object parameter) {
        if (Target.DataContext is GPIOViewModel viewModel) {
            viewModel.FilterChanged += OnFilterChanged;
        }
    }

    private void OnFilterChanged() {
        if (Target.DataContext is not GPIOViewModel viewModel) {
            return;
        }

        viewModel.CollectionView.Filter = e => {
            if (e is SolutionExplorerEvent.Model model) {
                if (model.Name.ToLower().Contains(viewModel.FilterText.ToLower())) {
                    return true;
                }

                if (model.Children != null) {
                    foreach (SolutionExplorerEvent.Model child in model.Children) {
                        if (child.Name.ToLower().Contains(viewModel.FilterText.ToLower())) {
                            return true;
                        }
                    }
                }
            }

            return false;
        };
        Target.ExpandAll();
    }
}