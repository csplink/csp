using CSP.Modules.Pages.MCU.Models.Description;
using CSP.Modules.Pages.MCU.Tools;
using CSP.Utils;
using Prism.Commands;
using Prism.Events;
using Prism.Mvvm;
using Prism.Regions;
using Serilog;
using System;
using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Media;

namespace CSP.Modules.Pages.MCU.ViewModels
{
    public class ClockTreeViewModel : BindableBase
    {
        private readonly IEventAggregator _eventAggregator;
        private readonly IRegionManager _regionManager;
        private Canvas _canvasControl;
        private double _canvasHeight = 900;
        private double _canvasWidth = 1600;
        private Uri _clockTreeImage;

        public ClockTreeViewModel(IRegionManager regionManager, IEventAggregator eventAggregator) {
            _regionManager = regionManager;
            _eventAggregator = eventAggregator;

            var path =
                $"{DescriptionHelper.RepositoryPath}/description/{DescriptionHelper.Name.ToLower()}/clock/{DescriptionHelper.MCU.Name}.svg";
            DebugUtil.Assert(File.Exists(path), new FileNotFoundException(nameof(path)), $"{path}: 不存在");
            if (File.Exists(path))
                ClockTreeImage = new Uri(path, UriKind.Relative);

            CanvasHeight = DescriptionHelper.Clock.Height;
            CanvasWidth = DescriptionHelper.Clock.Width;
        }

        public Canvas CanvasControl {
            get => _canvasControl;
            private set {
                if (SetProperty(ref _canvasControl, value)) {
                    foreach (var control in DescriptionHelper.Clock.ControlMap) {
                        UIElement obj = null;
                        switch (control.Value.Type) {
                            case "TextBox": {
                                    obj = ClockTreeViewModelTools.CreateTextBox(control.Value);
                                    break;
                                }
                            case "ComboBox": {
                                    obj = ClockTreeViewModelTools.CreateComboBox(control.Value);
                                    break;
                                }
                            case "Label": {
                                    obj = ClockTreeViewModelTools.CreateLabel(control.Value);
                                    break;
                                }
                            case "RadioButton": {
                                    obj = ClockTreeViewModelTools.CreateRadioButton(control.Value);
                                    break;
                                }
                            default: {
                                    Log.Warning($"不存在的CanvasControl: {control.Value.Type}");
                                    break;
                                }
                        }
                        if (obj != null) {
#if DEBUG
                            var binding = new Binding("Name") {
                                Mode = BindingMode.TwoWay,
                                Source = control.Value,
                                UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
                            };
                            BindingOperations.SetBinding(obj, FrameworkElement.ToolTipProperty, binding);
#endif
                            Canvas.SetLeft(obj, control.Value.X);
                            Canvas.SetTop(obj, control.Value.Y);
                            CanvasControl.Children.Add(obj);
                        }
                    }
                }
            }
        }

        public double CanvasHeight {
            get => _canvasHeight;
            set => SetProperty(ref _canvasHeight, value);
        }

        public double CanvasWidth {
            get => _canvasWidth;
            set => SetProperty(ref _canvasWidth, value);
        }

        public Uri ClockTreeImage {
            get => _clockTreeImage;
            set => SetProperty(ref _clockTreeImage, value);
        }

        public DelegateCommand<object> OnLoaded {
            get {
                return new DelegateCommand<object>((obj) => {
                    if (obj is not Canvas canvas)
                        return;

                    CanvasControl = canvas;
                });
            }
        }
    }

    internal class ClockTreeViewModelTools
    {
        public static TextBox CreateTextBox(ClockModel.ControlModel control) {
            TextBox box = new() {
                Width = control.Width,
                Height = control.Height,
                TextAlignment = TextAlignment.Center,
                BorderBrush = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#000000")!)
            };

            var binding = new Binding("Value") {
                Mode = BindingMode.TwoWay,
                Source = control,
                UpdateSourceTrigger = UpdateSourceTrigger.LostFocus
            };
            BindingOperations.SetBinding(box, TextBox.TextProperty, binding);

            return box;
        }

        public static ComboBox CreateComboBox(ClockModel.ControlModel control) {
            ComboBox box = new() {
                Width = control.Width,
                Height = control.Height,
                HorizontalContentAlignment = HorizontalAlignment.Center,
                BorderBrush = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#000000")!)
            };

            var binding = new Binding("Sources") {
                Mode = BindingMode.TwoWay,
                Source = control,
                UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
            };
            BindingOperations.SetBinding(box, ComboBox.ItemsSourceProperty, binding);
            box.DisplayMemberPath = "Text";
            if (control.Multiple == -114514)
                box.SelectedIndex = Convert.ToInt32(control.DefaultValue);

            box.SelectionChanged += (sender, e) => {
            };

            return box;
        }

        public static TextBox CreateLabel(ClockModel.ControlModel control) {
            TextBox box = new() {
                Width = control.Width,
                Height = control.Height,
                TextAlignment = TextAlignment.Center,
                VerticalContentAlignment = VerticalAlignment.Center,
                BorderBrush = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#000000")!),
                Style = null,
                IsReadOnly = true
            };

            SetLabelStatus(ref box, control);
            DescriptionHelper.Defines.PropertyChanged += (sender, e) => {
                SetLabelStatus(ref box, control);
            };

            return box;
        }

        private static void SetLabelStatus(ref TextBox label, ClockModel.ControlModel control) {
            foreach (var status in control.Status) {
                var b = true;
                foreach (var dependence in status.Dependencies) {
                    if (DescriptionHelper.Defines.ContainsKey(dependence.Key)) {
                        switch (dependence.Comparator) {
                            case "==":
                                if (DescriptionHelper.Defines[dependence.Key] != dependence.Value)
                                    b = false;
                                break;

                            case "<":
                                break;

                            case ">":
                                break;

                            case ">=":
                                break;

                            case "<=":
                                break;
                        }
                    }
                    else {
                        b = false;
                    }
                }

                if (b) {
                    foreach (var style in status.Styles) {
                        switch (style.Name) {
                            case "Text":
                                label.Text = style.Value;
                                break;

                            case "Style":
                                SetLabelStyle(ref label, style.Value);
                                break;
                        }
                    }
                }
            }
        }

        private static void SetLabelStyle(ref TextBox label, string style) {
            switch (style) {
                case "Disable":
                    label.Background = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#e7ddb8")!);
                    break;

                case "Enable":
                    label.Background = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#b0ce95")!);
                    break;
            }
        }

        public static Viewbox CreateRadioButton(ClockModel.ControlModel control) {
            Viewbox box = new() {
                Width = control.Width,
                Height = control.Height
            };
            RadioButton button = new() {
                GroupName = control.GroupName,
                BorderBrush = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#000000")!),
            };
            if (control.DefaultValue == 1 && control.Multiple == -114514)
                button.IsChecked = true;

            DescriptionHelper.Defines.CollectionChanged += (sender, e) => {
            };
            DescriptionHelper.Defines.PropertyChanged += (sender, e) => {
            };

            box.Child = button;

            return box;
        }
    }
}