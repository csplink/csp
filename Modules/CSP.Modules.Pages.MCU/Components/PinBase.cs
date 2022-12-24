using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using CSP.Components.ValuePropertyGrid;
using CSP.Events;
using CSP.Models.HAL.Config;
using CSP.Models.Internal;
using CSP.Singleton.HAL.Config;
using CSP.Singleton.Internal;
using CSP.Utils;
using Prism.Events;
using Prism.Ioc;

namespace CSP.Modules.Pages.MCU.Components;

using ip_t = Dictionary<string, Dictionary<string, string[]>>;

public class PinBase : UserControl
{
    public static readonly DependencyProperty PinProperty = DependencyProperty.Register(nameof(Pin),
        typeof(string),
        typeof(PinBase),
        new FrameworkPropertyMetadata(string.Empty, OnPinChanged) { BindsTwoWayByDefault = true });

    private readonly IEventAggregator _eventAggregator;
    private readonly MenuItem         _menuLock  = new() { Header = "锁定" };
    private readonly MenuItem         _menuReset = new() { Header = "重置" };
    private          PinConfigModel   _pinConfig;
    private          PinoutModel      _pinout;

    protected PinBase() {
        _menuLock.Click  += OnMenuLockClick;
        _menuReset.Click += OnMenuResetClick;

        IContainerExtension containerExtension = ContainerLocator.Current;
        _eventAggregator = containerExtension.Resolve<IEventAggregator>();
    }

    public string Pin {
        get => (string)GetValue(PinProperty);
        set => SetValue(PinProperty, value);
    }

    protected bool IsDirection { get; init; } = true;

    protected Button PinName { get; init; }

    protected TextBlock PinNote { get; init; }

    protected ContextMenu RightContextMenu { get; init; }

    protected void OnPinNameClick(object sender, MouseButtonEventArgs e) {
        if (string.IsNullOrWhiteSpace(_pinConfig.Function.String)) {
            _pinConfig.Property.Attributes.Clear();
            _pinConfig.Property.Details.Clear();

            foreach (var (detailName, detail) in _pinConfig.GetDetails()) {
                if (!_pinConfig.Property.Details.ContainsKey(detailName)) {
                    _pinConfig.Property.Details.Add(detailName, detail);
                }
            }

            foreach (var (attributeName, attribute) in _pinConfig.GetAttributes()) {
                if (!_pinConfig.Property.Attributes.ContainsKey(attributeName)) {
                    _pinConfig.Property.Attributes.Add(attributeName, attribute);
                }
            }
        }

        UpdateProperty();
    }

    protected void UpdateProperty() {
        _eventAggregator.GetEvent<PropertyEvent>().Publish(null);
        _eventAggregator.GetEvent<PropertyEvent>().Publish(_pinConfig.Property);
    }

    private static List<MenuItem> AddRightContextMenu(ItemsControl contextMenu, PinoutModel pin) {
        if (pin.Functions == null) {
            return null;
        }

        List<MenuItem> items = new();

        contextMenu.Items.Add(new Separator());
        foreach (MenuItem menu in pin.Functions.Select(static item => new MenuItem { Header = item.Key })) {
            items.Add(menu);
            contextMenu.Items.Add(menu);
        }

        return items;
    }

    private static void OnPinChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        ((PinBase)d).OnPinValueChanged(e);
    }

    private void InitPinNameStatus(string type) {
        if (PinName == null) {
            return;
        }

        switch (type) {
        case "I/O": {
            if (ColorConverter.ConvertFromString("#B9C4CA") is Color color) {
                PinName.Background  = new SolidColorBrush(color);
                PinName.BorderBrush = new SolidColorBrush(color);
            }

            PinName.Foreground = new SolidColorBrush(Colors.Black);

            break;
        }
        case "Reset":
        case "Boot": {
            if (ColorConverter.ConvertFromString("#BBCC00") is Color color) {
                PinName.Background  = new SolidColorBrush(color);
                PinName.BorderBrush = new SolidColorBrush(color);
            }

            PinName.Foreground = new SolidColorBrush(Colors.Black);

            break;
        }
        case "Power": {
            if (ColorConverter.ConvertFromString("#FFF6CC") is Color color) {
                PinName.Background  = new SolidColorBrush(color);
                PinName.BorderBrush = new SolidColorBrush(color);
            }

            PinName.Foreground = new SolidColorBrush(Colors.Black);

            break;
        }
        case "NC": {
            if (ColorConverter.ConvertFromString("#DCCFC0") is Color color) {
                PinName.Background  = new SolidColorBrush(color);
                PinName.BorderBrush = new SolidColorBrush(color);
            }

            PinName.Foreground = new SolidColorBrush(Colors.Black);

            break;
        }
        default: {
            if (ColorConverter.ConvertFromString("#B9C4CA") is Color color) {
                PinName.Background  = new SolidColorBrush(color);
                PinName.BorderBrush = new SolidColorBrush(color);
            }

            PinName.Foreground = new SolidColorBrush(Colors.Black);

            break;
        }
        }
    }

    private void OnMenuFunctionClick(object sender, RoutedEventArgs e) {
        if (sender is not MenuItem { Header: string name }) {
            return;
        }

        SetLocked(_menuLock, _pinout, true);
        SetFunction(name);
        UpdatePinNote();
    }

    private void OnMenuLockClick(object sender, RoutedEventArgs e) {
        if (sender is not MenuItem { Header: string str }) {
            return;
        }

        switch (str) {
        case "锁定":
            SetLocked(_menuLock, _pinout, true);

            break;

        case "解锁":
            SetLocked(_menuLock, _pinout, false);

            break;
        }
    }

    private void OnMenuResetClick(object sender, RoutedEventArgs e) {
        SetLocked(_menuLock, _pinout, false);
        SetFunction("");
    }

    private void OnPinValueChanged(DependencyPropertyChangedEventArgs e) {
        if (e.NewValue is not string name) {
            return;
        }

        if (PinName == null || PinNote == null || RightContextMenu == null) {
            return;
        }

        _pinout    = PinoutSingleton.Pinouts[name];
        _pinConfig = PinConfigSingleton.PinConfigs[name];

        if (IsDirection) {
            PinName.Content = name;
        }

        PinNote.Text = string.IsNullOrWhiteSpace(_pinConfig.Label.String) ? name : _pinConfig.Label.String;

        InitPinNameStatus(_pinout.Type);

        RightContextMenu.Items.Clear();

        RightContextMenu.Items.Add(_menuLock);
        RightContextMenu.Items.Add(new Separator());
        RightContextMenu.Items.Add(_menuReset);

        List<MenuItem> menuItems = AddRightContextMenu(RightContextMenu, _pinout);
        if (menuItems != null) {
            foreach (MenuItem menu in menuItems) {
                menu.Click += OnMenuFunctionClick;
            }
        }

        _pinConfig.Label.PropertyChanged += (sender, propertyChangedEventArgs) => { UpdatePinNote(); };
        _pinConfig.IsLocked.PropertyChanged += (sender, propertyChangedEventArgs) => {
            if (sender is not BooleanEditorModel model) {
                return;
            }

            SetLocked(_menuLock, _pinout, model.Boolean);
        };
    }

    private void SetFunction(string functionName) {
        if (PinName == null || PinNote == null || RightContextMenu == null) {
            return;
        }

        _pinConfig.Function.String = functionName;

        _pinConfig.Property.Attributes.Clear();
        _pinConfig.Property.Details.Clear();

        PinNote.Text = "";

        if (string.IsNullOrWhiteSpace(functionName)) {
            return;
        }

        if (!_pinout.Functions.ContainsKey(functionName)) {
            return;
        }

        if (string.IsNullOrWhiteSpace(_pinout.Functions[functionName].Type)) {
            return;
        }

        switch (_pinout.Functions[functionName].Type.ToLower()) {
        case "gpio": {
            MapModel gpioMap = MapSingleton.Maps["gpio"];
            ip_t     gpioIP  = IPSingleton.IP["gpio"];

            if (gpioMap == null || gpioIP == null) {
                break;
            }

            if (_pinout.Functions[functionName].Mode != null) {
                string modeName = _pinout.Functions[functionName].Mode;
                foreach (var (parameterName, parameter) in gpioIP[modeName]) {
                    ObservableDictionary<string, string> map = new();

                    foreach (string value in parameter) {
                        if (gpioMap.Total.ContainsKey(value)) {
                            map.Add(value, gpioMap.Total[value]);
                        }
                    }

                    DictionaryEditorModel model = new() {
                        Source = map
                    };
                    model.PropertyChanged += (sender, e) => {
                        if (sender is not DictionaryEditorModel) {
                            return;
                        }

                        switch (e.PropertyName) {
                        case "String": {
                            break;
                        }
                        }
                    };
                    _pinConfig.Property.Details.Add(parameterName, model);
                    _pinConfig.Property.Attributes.Add(parameterName, gpioMap.Attributes[parameterName]);
                }
            }

            break;
        }
        }

        foreach (var (detailName, detail) in _pinConfig.GetDetails()) {
            if (!_pinConfig.Property.Details.ContainsKey(detailName)) {
                _pinConfig.Property.Details.Add(detailName, detail);
            }
        }

        foreach (var (attributeName, attribute) in _pinConfig.GetAttributes()) {
            if (!_pinConfig.Property.Attributes.ContainsKey(attributeName)) {
                _pinConfig.Property.Attributes.Add(attributeName, attribute);
            }
        }

        UpdateProperty();
    }

    private void SetLocked(MenuItem menuLock, PinoutModel pin, bool value) {
        if (menuLock == null || PinName == null) {
            return;
        }

        _pinConfig.IsLocked.Boolean = value;

        menuLock.Header = value ? "解锁" : "锁定";
        if (pin.Type != null) {
            SetPinNameStatus(pin.Type, value);
        }
    }

    private void SetPinNameStatus(string type, bool isLock) {
        if (PinName == null) {
            return;
        }

        if (isLock) {
            if (ColorConverter.ConvertFromString("#00CC44") is Color color) {
                PinName.Background  = new SolidColorBrush(color);
                PinName.BorderBrush = new SolidColorBrush(color);
            }

            PinName.Foreground = new SolidColorBrush(Colors.Black);
        }
        else {
            InitPinNameStatus(type);
        }
    }

    private void UpdatePinNote() {
        if (PinNote == null) {
            return;
        }

        PinNote.Text = string.IsNullOrWhiteSpace(_pinConfig.Label.String)
            ? _pinConfig.Function.String
            : $"{_pinConfig.Label.String}: ({_pinConfig.Function.String})";
    }
}