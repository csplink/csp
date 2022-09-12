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
            _eventAggregator.GetEvent<PropertyEvent>().Publish(Property);
        }

        #endregion INavigationAware

        private readonly IEventAggregator _eventAggregator;

        public ClockViewModel(IEventAggregator eventAggregator) {
            _eventAggregator = eventAggregator;

            var clockMap = DescriptionHelper.GetMap("Clock");
            var clockIP = DescriptionHelper.GetIP("Clock");
            foreach (var mode in clockIP.ModeMap) {
                foreach (var parameter in clockIP.ModeMap[mode.Key].Parameters) {
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
                    Property.Details.Add(parameter.Key, model);
                    Property.Attributes.Add(parameter.Key, clockMap.Attributes[parameter.Key]);
                }
            }
        }

        public PropertyDetails Property { get; } = new();
    }
}