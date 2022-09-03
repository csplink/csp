using CSP.Modules.Pages.MCU.Models.Repository;
using CSP.Utils.Extensions;
using Prism.Events;
using Prism.Ioc;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
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

        protected void OnPinNameClick(object sender, RoutedEventArgs e) {
            UpdateProperty();
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

            SetFunction(name);
            UpdatePinNote(Pin);
            SetLocked(_menuLock, Pin, true);
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
            SetFunction(null);
        }

        private void OnPinPropertyChanged(object sender, PropertyChangedEventArgs e) {
            // if (sender is not PinoutModel.PinModel.DataContextModel)
            //     return;
            //
            // if (e.PropertyName == "Label")
            //     UpdatePinNote(Pin);
        }

        private void OnPinValueChanged(DependencyPropertyChangedEventArgs e) {
            if (e.NewValue is not PinoutModel.PinModel pin)
                return;
            if (PinName == null || PinNote == null || RightContextMenu == null)
                return;

            PinName.Content = pin.Name;
            // PinNote.Text = pin.BaseProperty.Label;

            InitPinNameStatus(pin.Type);

            RightContextMenu.Items.Clear();

            RightContextMenu.Items.Add(_menuLock);
            RightContextMenu.Items.Add(new Separator());
            RightContextMenu.Items.Add(_menuReset);

            var menuItems = AddRightContextMenu(RightContextMenu, pin);
            foreach (var menu in menuItems) {
                menu.Click += OnMenuFunctionClick;
            }

            // pin.BaseProperty.PropertyChanged += OnPinPropertyChanged;
        }

        private void SetFunction(string functionName) {
            if (PinName == null || PinNote == null || RightContextMenu == null)
                return;

            // Pin.BaseProperty.Function = functionName;
            //
            // Pin.GPIOProperty.Attributes.Clear();
            // Pin.GPIOProperty.Details.Clear();

            PinNote.Text = "";

            if (functionName == null) {
                return;
            }

            if (!Pin.FunctionMap.ContainsKey(functionName))
                return;

            if (Pin.FunctionMap[functionName].Type.IsNullOrEmpty())
                return;

            // var gpio = MCUHelper.GetMap("GPIO");
            // if (gpio == null)
            //     return;
            //
            // switch (Pin.Functions[functionName].Type) {
            //     case "GPIO": {
            //             if (Pin.Functions[functionName].Mode != null) {
            //                 foreach (var parameter in Pin.Functions[functionName].Mode.Parameters) {
            //                     var map = new Dictionary<string, string>();
            //
            //                     // ReSharper disable once LoopCanBeConvertedToQuery
            //                     foreach (var value in parameter.Value.Values) {
            //                         if (gpio.Total.ContainsKey(value)) {
            //                             map.Add(value, gpio.Total[value]);
            //                         }
            //                     }
            //
            //                     var model = new MapModel.GroupModel.ValuePropertyGridComboEditorModel {
            //                         Source = map
            //                     };
            //                     Pin.GPIOProperty.Details.Add(parameter.Key, model);
            //                     Pin.GPIOProperty.Attributes.Add(parameter.Key, gpio.Attributes[parameter.Key]);
            //                 }
            //             }
            //         }
            //         break;
            // }

            UpdateProperty();
        }

        private void SetLocked(HeaderedItemsControl menuLock, PinoutModel.PinModel pin, bool value) {
            if (menuLock == null || PinName == null)
                return;

            // Pin.BaseProperty.IsLocked = value;

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

        private void UpdatePinNote(PinoutModel.PinModel pin) {
            if (PinNote == null)
                return;

            // PinNote.Text = Pin.BaseProperty.Label.IsNullOrEmpty() ?
            //     Pin.BaseProperty.Function :
            //     $"{Pin.BaseProperty.Label}: ({Pin.BaseProperty.Function})";
        }

        private void UpdateProperty() {
            // _eventAggregator.GetEvent<PropertyEvent>().Publish(Pin.GPIOProperty);
        }
    }
}