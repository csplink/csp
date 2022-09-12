using CSP.Events;
using CSP.Modules.Pages.MCU.Components.ValuePropertyGrid;
using CSP.Modules.Pages.MCU.Models;
using CSP.Modules.Pages.MCU.Models.Repository;
using CSP.Modules.Pages.MCU.Tools;
using CSP.Utils;
using CSP.Utils.Extensions;
using Prism.Events;
using Prism.Ioc;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;

namespace CSP.Modules.Pages.MCU.Components.LQFP
{
    public class PinBase : UserControl
    {
        public static readonly DependencyProperty PinProperty = DependencyProperty.Register(nameof(Pin),
            typeof(PinoutModel.PinModel),
            typeof(PinBase),
            new FrameworkPropertyMetadata(new PinoutModel.PinModel(), OnPinChanged) { BindsTwoWayByDefault = true });

        private readonly IEventAggregator _eventAggregator;
        private readonly MenuItem _menuLock = new() { Header = "锁定" };
        private readonly MenuItem _menuReset = new() { Header = "重置" };
        private PinModel _pinProperty;

        protected PinBase() {
            _menuLock.Click += OnMenuLockClick;
            _menuReset.Click += OnMenuResetClick;

            var containerExtension = ContainerLocator.Current;
            _eventAggregator = containerExtension.Resolve<IEventAggregator>();
        }

        public PinoutModel.PinModel Pin {
            get => (PinoutModel.PinModel)GetValue(PinProperty);
            set => SetValue(PinProperty, value);
        }

        protected Button PinName { get; set; }

        protected TextBlock PinNote { get; set; }

        protected ContextMenu RightContextMenu { get; set; }

        protected void OnPinNameClick(object sender, MouseButtonEventArgs e) {
            if (_pinProperty.Function.IsNullOrEmpty()) {
                _pinProperty.Property.Attributes.Clear();
                _pinProperty.Property.Details.Clear();

                foreach (var details in _pinProperty.GetDetails()) {
                    if (!_pinProperty.Property.Details.ContainsKey(details.Key))
                        _pinProperty.Property.Details.Add(details);
                }

                foreach (var attributes in _pinProperty.GetAttributes()) {
                    if (!_pinProperty.Property.Attributes.ContainsKey(attributes.Key))
                        _pinProperty.Property.Attributes.Add(attributes);
                }
            }

            UpdateProperty();
        }

        protected void UpdateProperty() {
            _eventAggregator.GetEvent<PropertyEvent>().Publish(_pinProperty.Property);
        }

        private static List<MenuItem> AddRightContextMenu(ItemsControl contextMenu, PinoutModel.PinModel pin) {
            if (pin.FunctionMap == null)
                return null;

            var items = new List<MenuItem>();

            contextMenu.Items.Add(new Separator());
            foreach (var menu in pin.FunctionMap.Select(static item => new MenuItem { Header = item.Key })) {
                items.Add(menu);
                contextMenu.Items.Add(menu);
            }

            return items;
        }

        private static void OnPinChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
            ((PinBase)d).OnPinValueChanged(e);
        }

        private void InitPinNameStatus(string type) {
            if (PinName == null)
                return;
            switch (type) {
                case "I/O": {
                        if (ColorConverter.ConvertFromString("#B9C4CA") is Color color) {
                            PinName.Background = new SolidColorBrush(color);
                            PinName.BorderBrush = new SolidColorBrush(color);
                        }

                        PinName.Foreground = new SolidColorBrush(Colors.Black);
                        break;
                    }
                case "Reset":
                case "Boot": {
                        if (ColorConverter.ConvertFromString("#BBCC00") is Color color) {
                            PinName.Background = new SolidColorBrush(color);
                            PinName.BorderBrush = new SolidColorBrush(color);
                        }

                        PinName.Foreground = new SolidColorBrush(Colors.Black);
                        break;
                    }
                case "Power": {
                        if (ColorConverter.ConvertFromString("#FFF6CC") is Color color) {
                            PinName.Background = new SolidColorBrush(color);
                            PinName.BorderBrush = new SolidColorBrush(color);
                        }

                        PinName.Foreground = new SolidColorBrush(Colors.Black);
                        break;
                    }
                case "NC": {
                        if (ColorConverter.ConvertFromString("#DCCFC0") is Color color) {
                            PinName.Background = new SolidColorBrush(color);
                            PinName.BorderBrush = new SolidColorBrush(color);
                        }

                        PinName.Foreground = new SolidColorBrush(Colors.Black);
                        break;
                    }
                default: {
                        if (ColorConverter.ConvertFromString("#B9C4CA") is Color color) {
                            PinName.Background = new SolidColorBrush(color);
                            PinName.BorderBrush = new SolidColorBrush(color);
                        }

                        PinName.Foreground = new SolidColorBrush(Colors.Black);
                        break;
                    }
            }
        }

        private void OnMenuFunctionClick(object sender, RoutedEventArgs e) {
            if (sender is not MenuItem { Header: string name })
                return;

            SetLocked(_menuLock, Pin, true);
            SetFunction(name);
            UpdatePinNote();
        }

        private void OnMenuLockClick(object sender, RoutedEventArgs e) {
            if (sender is not MenuItem { Header: string str })
                return;

            switch (str) {
                case "锁定":
                    SetLocked(_menuLock, Pin, true);
                    break;

                case "解锁":
                    SetLocked(_menuLock, Pin, false);
                    break;
            }
        }

        private void OnMenuResetClick(object sender, RoutedEventArgs e) {
            SetLocked(_menuLock, Pin, false);
            SetFunction("");
        }

        private void OnPinValueChanged(DependencyPropertyChangedEventArgs e) {
            if (e.NewValue is not PinoutModel.PinModel pin)
                return;
            if (PinName == null || PinNote == null || RightContextMenu == null)
                return;
            _pinProperty = DescriptionHelper.GetPinProperty(pin.Name);

            PinName.Content = pin.Name;
            PinNote.Text = _pinProperty.Label;

            InitPinNameStatus(pin.Type);

            RightContextMenu.Items.Clear();

            RightContextMenu.Items.Add(_menuLock);
            RightContextMenu.Items.Add(new Separator());
            RightContextMenu.Items.Add(_menuReset);

            var menuItems = AddRightContextMenu(RightContextMenu, pin);
            foreach (var menu in menuItems) {
                menu.Click += OnMenuFunctionClick;
            }
            _pinProperty.PropertyChanged += (sender, propertyChangedEventArgs) => {
                if (sender is not PinModel)
                    return;

                if (propertyChangedEventArgs.PropertyName == "Label")
                    UpdatePinNote();
            };
        }

        private void SetFunction(string functionName) {
            if (PinName == null || PinNote == null || RightContextMenu == null)
                return;

            _pinProperty.Function = functionName;

            _pinProperty.Property.Attributes.Clear();
            _pinProperty.Property.Details.Clear();

            PinNote.Text = "";

            if (functionName.IsNullOrEmpty()) {
                return;
            }

            if (!Pin.FunctionMap.ContainsKey(functionName))
                return;

            if (Pin.FunctionMap[functionName].Type.IsNullOrEmpty())
                return;

            switch (Pin.FunctionMap[functionName].Type) {
                case "GPIO": {
                        var gpioMap = DescriptionHelper.GetMap("GPIO");
                        var gpioIP = DescriptionHelper.GetIP("GPIO");
                        if (gpioMap == null || gpioIP == null)
                            break;
                        if (Pin.FunctionMap[functionName].Mode != null) {
                            var modeName = Pin.FunctionMap[functionName].Mode;
                            foreach (var parameter in gpioIP.ModeMap[modeName].Parameters) {
                                var map = new ObservableDictionary<string, string>();

                                foreach (var value in parameter.Value.Values) {
                                    if (gpioMap.Total.ContainsKey(value)) {
                                        map.Add(value, gpioMap.Total[value]);
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
                                _pinProperty.Property.Details.Add(parameter.Key, model);
                                _pinProperty.Property.Attributes.Add(parameter.Key, gpioMap.Attributes[parameter.Key]);
                            }
                        }
                        break;
                    }
            }

            foreach (var details in _pinProperty.GetDetails()) {
                if (!_pinProperty.Property.Details.ContainsKey(details.Key))
                    _pinProperty.Property.Details.Add(details);
            }

            foreach (var attributes in _pinProperty.GetAttributes()) {
                if (!_pinProperty.Property.Attributes.ContainsKey(attributes.Key))
                    _pinProperty.Property.Attributes.Add(attributes);
            }

            UpdateProperty();
        }

        private void SetLocked(HeaderedItemsControl menuLock, PinoutModel.PinModel pin, bool value) {
            if (menuLock == null || PinName == null)
                return;

            _pinProperty.IsLocked = value;

            menuLock.Header = value ? "解锁" : "锁定";
            if (pin.Type != null)
                SetPinNameStatus(pin.Type, value);
        }

        private void SetPinNameStatus(string type, bool isLock) {
            if (PinName == null)
                return;

            if (isLock) {
                if (ColorConverter.ConvertFromString("#00CC44") is Color color) {
                    PinName.Background = new SolidColorBrush(color);
                    PinName.BorderBrush = new SolidColorBrush(color);
                }

                PinName.Foreground = new SolidColorBrush(Colors.Black);
            }
            else {
                InitPinNameStatus(type);
            }
        }

        private void UpdatePinNote() {
            if (PinNote == null)
                return;

            PinNote.Text = _pinProperty.Label.IsNullOrEmpty() ? _pinProperty.Function : $"{_pinProperty.Label}: ({_pinProperty.Function})";
        }
    }
}