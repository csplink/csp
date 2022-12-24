using System;
using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Media;
using CSP.Models.HAL.Config;
using CSP.Resources;
using CSP.Singleton.DB;
using CSP.Singleton.DB.Chip;
using CSP.Singleton.HAL.Config;
using CSP.Singleton.Internal;
using CSP.Utils;
using Prism.Commands;
using Prism.Events;
using Prism.Mvvm;
using Prism.Regions;
using Serilog;

namespace CSP.Modules.Pages.MCU.ViewModels;

public class ClockTreeViewModel : BindableBase
{
    private readonly IEventAggregator _eventAggregator;
    private readonly IRegionManager   _regionManager;
    private          Canvas           _canvasControl;
    private          double           _canvasHeight = 900;
    private          double           _canvasWidth  = 1600;
    private          Uri              _clockTreeImage;

    public ClockTreeViewModel(IRegionManager regionManager, IEventAggregator eventAggregator) {
        _regionManager   = regionManager;
        _eventAggregator = eventAggregator;

        string name     = SummarySingleton.Summary.Name;
        string repo     = ConfigFile.PathRepo;
        string category = PackageSingleton.Package.Category;
        string package  = PackageSingleton.Package.Name;
        string path     = $"{repo}/repositories/{category}/{package}/latest/config/{name}/clock/{name}.svg";
        DebugUtil.Assert(File.Exists(path), new FileNotFoundException(nameof(path)), $"{path}: 不存在");
        if (File.Exists(path)) {
            ClockTreeImage = new Uri(path, UriKind.Relative);
        }

        CanvasHeight = ClockSingleton.Clock.Height;
        CanvasWidth  = ClockSingleton.Clock.Width;
    }

    public Canvas CanvasControl {
        get => _canvasControl;
        private set {
            if (SetProperty(ref _canvasControl, value)) {
                CreateControl();
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

    public DelegateCommand<object> OnLoaded =>
        new(obj => {
            if (obj is not Canvas canvas) {
                return;
            }

            CanvasControl = canvas;
        });

    private void CreateControl() {
        // 第一遍轮询创建控件
        foreach (var (controlID, control) in ClockSingleton.Clock.Controls) {
            UIElement obj    = null;
            float     x      = ClockSingleton.Clock.Shapes[controlID].X;
            float     y      = ClockSingleton.Clock.Shapes[controlID].Y;
            float     width  = ClockSingleton.Clock.Shapes[controlID].Width;
            float     height = ClockSingleton.Clock.Shapes[controlID].Height;
            switch (control.Base.Type) {
            case "TextBox":
                obj = ClockTreeViewModelTools.CreateTextBox(control, width, height);

                break;

            case "ComboBox":
                obj = ClockTreeViewModelTools.CreateComboBox(control, width, height);

                break;

            case "Label":
                obj = ClockTreeViewModelTools.CreateLabel(control, width, height);

                break;

            case "RadioButton":
                obj = ClockTreeViewModelTools.CreateRadioButton(control, width, height);

                break;

            default:
                Log.Warning($"不存在的CanvasControl: {control.Base.Type}");

                break;
            }

            if (obj != null) {
#if DEBUG
                Binding binding = new("Name") {
                    Mode                = BindingMode.TwoWay,
                    Source              = control,
                    UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
                };
#else
                Binding binding = new("Value") {
                    Mode = BindingMode.TwoWay,
                    Source = control,
                    UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
                };
#endif
                BindingOperations.SetBinding(obj, FrameworkElement.ToolTipProperty, binding);
                Canvas.SetLeft(obj, ClockSingleton.Clock.Shapes[controlID].X);
                Canvas.SetTop(obj, ClockSingleton.Clock.Shapes[controlID].Y);
                CanvasControl.Children.Add(obj);
            }
        }

        // 第二次轮询进行变量初始化
        foreach (var (_, control) in ClockSingleton.Clock.Controls) {
            control.DisplayValue = control.DefaultValue;
            switch (control.Base.Type) {
            case "RadioButton":
                if (control.Base.IsChecked) {
                    ProjectSingleton.ChangeDefine(null, $"CSP_USING_{control.Base.Macro}", null);
                }

                break;
            }
        }
    }
}

internal class ClockTreeViewModelTools
{
    public static TextBox CreateTextBox(ClockModel.ControlModel control, float width, float height) {
        TextBox box = new() {
            Width         = width,
            Height        = height,
            TextAlignment = TextAlignment.Center,
            BorderBrush   = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#000000")!)
        };

        Binding binding = new("DisplayValue") {
            Mode                = BindingMode.TwoWay,
            Source              = control,
            UpdateSourceTrigger = UpdateSourceTrigger.LostFocus
        };
        BindingOperations.SetBinding(box, TextBox.TextProperty, binding);

        return box;
    }

    public static ComboBox CreateComboBox(ClockModel.ControlModel control, float width, float height) {
        ComboBox box = new() {
            Width                      = width,
            Height                     = height,
            HorizontalContentAlignment = HorizontalAlignment.Center,
            BorderBrush                = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#000000")!)
        };

        Binding binding = new("Signals") {
            Mode                = BindingMode.TwoWay,
            Source              = control,
            UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
        };
        BindingOperations.SetBinding(box, ComboBox.ItemsSourceProperty, binding);
        box.DisplayMemberPath = "Text";
        // box.SelectedIndex     = control.DefaultIndex;
        //
        // box.SelectionChanged += (sender, e) => {
        //     string s = "";
        //     foreach (var signal1 in control.Signals) {
        //         if (DescriptionHelper.IsDependence(signal1.DependenceArray)) {
        //             s = signal1.Source;
        //         }
        //     }
        //
        //     if (box.SelectedItem is ClockModel.ControlModel.SignalModel signal2 && !s.IsNullOrEmpty()) {
        //         if (DescriptionHelper.Clock.ControlMap.ContainsKey(s)) {
        //             var ctrl = DescriptionHelper.Clock.ControlMap[s];
        //             control.Value = signal2.Operator.ToLower() switch {
        //                 "/" => ctrl.Value / signal2.Value,
        //                 "*" => ctrl.Value * signal2.Value,
        //                 _   => control.Value
        //             };
        //         }
        //     }
        // };
        //
        // foreach (var ctl in DescriptionHelper.Clock.ControlMap) {
        //     foreach (var signal1 in control.Signals) {
        //         if (ctl.Value.Name == signal1.Source && DescriptionHelper.IsDependence(signal1.DependenceArray)) {
        //             ctl.Value.PropertyChanged += (sender, e) => {
        //                 string s = "";
        //                 foreach (var signal2 in control.Signals) {
        //                     if (DescriptionHelper.IsDependence(signal2.DependenceArray)) {
        //                         s = signal2.Source;
        //                     }
        //                 }
        //
        //                 if (box.SelectedItem is ClockModel.ControlModel.SignalModel signal3 && !s.IsNullOrEmpty()) {
        //                     if (DescriptionHelper.Clock.ControlMap.ContainsKey(s)) {
        //                         var ctrl = DescriptionHelper.Clock.ControlMap[s];
        //                         control.Value = signal3.Operator.ToLower() switch {
        //                             "/" => ctrl.Value / signal3.Value,
        //                             "*" => ctrl.Value * signal3.Value,
        //                             _   => control.Value
        //                         };
        //                     }
        //                 }
        //             };
        //         }
        //     }
        // }

        return box;
    }

    public static TextBox CreateLabel(ClockModel.ControlModel control, float width, float height) {
        TextBox box = new() {
            Width                    = width,
            Height                   = height,
            TextAlignment            = TextAlignment.Center,
            VerticalContentAlignment = VerticalAlignment.Center,
            BorderBrush              = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#000000")!),
            Style                    = null,
            IsReadOnly               = true
        };

        if (control.Base.Multiple != 0) {
            Binding binding = new("DisplayValue") {
                Mode                = BindingMode.TwoWay,
                Source              = control,
                UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
            };
            BindingOperations.SetBinding(box, TextBox.TextProperty, binding);
        }

        SetLabelStyle(ref box, control);
        ProjectSingleton.Project.Defines.PropertyChanged += (sender, e) => {
            SetLabelStyle(ref box, control);
            //     foreach (var signal in control.Signals) {
            //         if (DescriptionHelper.IsDependence(signal.DependenceArray)) {
            //             float value = 0;
            //             if (!signal.Source.IsNullOrEmpty()) {
            //                 if (DescriptionHelper.Clock.ControlMap.ContainsKey(signal.Source)) {
            //                     var ctrl = DescriptionHelper.Clock.ControlMap[signal.Source];
            //                     value = ctrl.Value;
            //                 }
            //                 //TODO 出现错误
            //             }
            //             else if (signal.SourceValue != 0) {
            //                 value = signal.SourceValue;
            //             }
            //
            //             //TODO 出现错误
            //             control.Value = signal.Operator.ToLower() switch {
            //                 "/" => value / signal.Value,
            //                 "*" => value * signal.Value,
            //                 _   => control.Value
            //             };
            //         }
            //     }
        };

        // foreach (var ctl in DescriptionHelper.Clock.ControlMap) {
        //     foreach (var signal in control.Signals) {
        //         if (ctl.Value.Name == signal.Source) {
        //             ctl.Value.PropertyChanged += (sender, e) => {
        //                 if (DescriptionHelper.IsDependence(signal.DependenceArray)) {
        //                     control.Value = signal.Operator.ToLower() switch {
        //                         "/" => ctl.Value.Value / signal.Value,
        //                         "*" => ctl.Value.Value * signal.Value,
        //                         _   => control.Value
        //                     };
        //                 }
        //             };
        //         }
        //     }
        // }

        return box;
    }

    private static void SetLabelStyle(ref TextBox label, ClockModel.ControlModel control) {
        if (control.Styles == null) {
            return;
        }

        foreach (var (_, style) in control.Styles) {
            if (ProjectSingleton.IsDependence(style.Dependencies)) {
                label.Text = style.Text["zh-cn"];
                SetLabelStatus(ref label, style.Status);
            }
        }
    }

    private static void SetLabelStatus(ref TextBox label, string style) {
        label.Background = style switch {
            "Disable" => new SolidColorBrush((Color)ColorConverter.ConvertFromString("#e7ddb8")!),
            "Enable"  => new SolidColorBrush((Color)ColorConverter.ConvertFromString("#b0ce95")!),
            _         => label.Background
        };
    }

    public static Viewbox CreateRadioButton(ClockModel.ControlModel control, float width, float height) {
        Viewbox box = new() {
            Width  = width,
            Height = height
        };
        RadioButton button = new() {
            // GroupName   = control.GroupName,
            // Tag         = control.Name,
            // BorderBrush = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#000000")!),
            // IsChecked   = control.IsChecked
        };

        // DescriptionHelper.Defines.PropertyChanged += (sender, e) => { };
        //
        // button.Checked += (sender, e) => {
        //     if (sender is RadioButton { IsChecked: true } rb) {
        //         string groupName = rb.GroupName;
        //         string name      = rb.Tag.ToString();
        //         foreach (var ctrl in DescriptionHelper.Clock.ControlMap) {
        //             if (ctrl.Value.GroupName == groupName) {
        //                 if (ctrl.Value.Name == name) {
        //                     DescriptionHelper.ChangeDefine(null, $"CSP_USING_{ctrl.Value.Macro}", null);
        //                 }
        //                 else {
        //                     DescriptionHelper.ChangeDefine($"CSP_USING_{ctrl.Value.Macro}", null, null);
        //                 }
        //             }
        //         }
        //     }
        // };

        box.Child = button;

        return box;
    }
}