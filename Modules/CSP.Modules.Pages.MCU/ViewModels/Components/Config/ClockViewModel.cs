using CSP.Components.ValuePropertyGrid;
using CSP.Events;
using CSP.Modules.Pages.MCU.Tools;
using CSP.Utils;
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
                var property = new PropertyDetails();
                var clockMap = DescriptionHelper.GetMap("Clock");
                var clockIP = DescriptionHelper.GetIP("Clock");
                foreach (var mode in clockIP.ModeMap) {
                    foreach (var parameter in clockIP.ModeMap[mode.Key].ParameterMap) {
                        var map = new ObservableDictionary<string, string>();

                        foreach (var value in parameter.Value.Values) {
                            if (clockMap.Total.ContainsKey(value)) {
                                map.Add(value, clockMap.Total[value]);
                            }
                        }

                        var model = new DictionaryEditorModel {
                            Source = map
                        };
                        model.PropertyChanged += (sender, e) => {
                            if (sender is not DictionaryEditorModel)
                                return;

                            switch (e.PropertyName) {
                                case "Value": {
                                    }

                                    break;
                            }
                        };
                        property.Details.Add(parameter.Key, model);
                        property.Attributes.Add(parameter.Key, clockMap.Attributes[parameter.Key]);
                    }
                }
                DescriptionHelper.Properties.Add("Clock", property);
            }
        }
    }
}