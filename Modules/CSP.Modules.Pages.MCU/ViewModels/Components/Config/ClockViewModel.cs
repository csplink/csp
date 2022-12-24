using CSP.Components.ValuePropertyGrid;
using CSP.Events;
using CSP.Models.HAL.Config;
using CSP.Singleton.HAL.Config;
using CSP.Singleton.Internal;
using CSP.Utils;
using Prism.Events;
using Prism.Mvvm;
using Prism.Regions;

namespace CSP.Modules.Pages.MCU.ViewModels.Components.Config;

public class ClockViewModel : BindableBase, INavigationAware
{
    private readonly IEventAggregator _eventAggregator;

    public ClockViewModel(IEventAggregator eventAggregator) {
        _eventAggregator = eventAggregator;

        if (!ProjectSingleton.Project.Properties.ContainsKey("clock")) {
            ProjectSingleton.Project.Properties.Add("clock", CreateClockPropertyDetails());
        }
    }

    public static PropertyDetails CreateClockPropertyDetails() {
        PropertyDetails property = new();
        MapModel clockMap = MapSingleton.Maps["clock"];
        ip_t clockIP = IPSingleton.IP["clock"];
        if (clockMap == null || clockIP == null) {
            MessageBoxUtil.Error("无 clock IP 与其 Map");

            return null;
        }

        foreach (var (_, mode) in clockIP) {
            foreach (var (parameterName, parameters) in mode) {
                ObservableDictionary<string, string> map = new();

                foreach (string value in parameters) {
                    if (clockMap.Total.ContainsKey(value)) {
                        map.Add(value, clockMap.Total[value]);
                    }
                }

                DictionaryEditorModel model = new() {
                    Source = map
                };
                model.PropertyValueChanged += (sender, e) => {
                    if (sender is not DictionaryEditorModel) {
                        return;
                    }

                    switch (e.PropertyName) {
                    case "Value": {
                        ProjectSingleton.ChangeDefine(e.OldValue != null ? $"CSP_USING_{e.OldValue}" : null,
                            e.NewValue != null ? $"CSP_USING_{e.NewValue}" : null, null);

                        break;
                    }
                    }
                };
                property.Details.Add(parameterName, model);
                property.Attributes.Add(parameterName, clockMap.Attributes[parameterName]);
            }
        }

        return property;
    }

    #region INavigationAware

    public bool IsNavigationTarget(NavigationContext navigationContext) {
        return false;
    }

    public void OnNavigatedFrom(NavigationContext navigationContext) {
    }

    public void OnNavigatedTo(NavigationContext navigationContext) {
        _eventAggregator.GetEvent<PropertyEvent>().Publish(null);
        if (ProjectSingleton.Project.Properties.ContainsKey("clock")) {
            PropertyDetails properties = ProjectSingleton.Project.Properties["clock"];
            _eventAggregator.GetEvent<PropertyEvent>().Publish(properties);
        }
    }

    #endregion INavigationAware
}