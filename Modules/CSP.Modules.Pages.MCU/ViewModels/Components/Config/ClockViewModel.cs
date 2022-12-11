﻿using CSP.Components.ValuePropertyGrid;
using CSP.Events;
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

        if (!DescriptionHelper.Properties.ContainsKey("Clock")) {
            DescriptionHelper.Properties.Add("Clock", CreateClockPropertyDetails());
        }
    }

    public static PropertyDetails CreateClockPropertyDetails() {
        PropertyDetails property = new PropertyDetails();
        var             clockMap = DescriptionHelper.GetMap("Clock");
        var             clockIP  = DescriptionHelper.GetIP("Clock");
        if (clockMap == null || clockIP == null) {
            MessageBoxUtil.Error("无 clock IP 与其 Map");

            return null;
        }

        foreach (var mode in clockIP.ModeMap) {
            foreach (var parameter in clockIP.ModeMap[mode.Key].ParameterMap) {
                ObservableDictionary<string, string> map = new ObservableDictionary<string, string>();

                foreach (var value in parameter.Value.Values) {
                    if (clockMap.Total.ContainsKey(value)) {
                        map.Add(value, clockMap.Total[value]);
                    }
                }

                DictionaryEditorModel model = new DictionaryEditorModel {
                    Source = map
                };
                model.PropertyValueChanged += (sender, e) => {
                    if (sender is not DictionaryEditorModel) {
                        return;
                    }

                    switch (e.PropertyName) {
                    case "Value": {
                        DescriptionHelper.ChangeDefine(e.OldValue != null ? $"CSP_USING_{e.OldValue}" : null,
                            e.NewValue != null ? $"CSP_USING_{e.NewValue}" : null, null);

                        break;
                    }
                    }
                };
                property.Details.Add(parameter.Key, model);
                property.Attributes.Add(parameter.Key, clockMap.Attributes[parameter.Key]);
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
        if (DescriptionHelper.Properties.ContainsKey("Clock")) {
            var properties = DescriptionHelper.Properties["Clock"];
            _eventAggregator.GetEvent<PropertyEvent>().Publish(properties);
        }
    }

    #endregion INavigationAware
}