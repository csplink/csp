using System;
using System.IO;
using System.Windows.Controls;
using CSP.Resources;
using CSP.Singleton.DB;
using CSP.Singleton.DB.Chip;
using CSP.Singleton.HAL.Config;
using CSP.Utils;
using Prism.Commands;
using Prism.Events;
using Prism.Mvvm;
using Prism.Regions;

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
                // CreateControl();
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

//     private void CreateControl() {
//         // 第一遍轮询创建控件
//         foreach (var control in ClockSingleton.Clock.ControlMap) {
//             UIElement obj = null;
//             switch (control.Value.Type) {
//             case "TextBox":
//                 obj = ClockTreeViewModelTools.CreateTextBox(control.Value);
//
//                 break;
//
//             case "ComboBox":
//                 obj = ClockTreeViewModelTools.CreateComboBox(control.Value);
//
//                 break;
//
//             case "Label":
//                 obj = ClockTreeViewModelTools.CreateLabel(control.Value);
//
//                 break;
//
//             case "RadioButton":
//                 obj = ClockTreeViewModelTools.CreateRadioButton(control.Value);
//
//                 break;
//
//             default:
//                 Log.Warning($"不存在的CanvasControl: {control.Value.Type}");
//
//                 break;
//             }
//
//             if (obj != null) {
// #if DEBUG
//                 Binding binding = new("Name") {
//                     Mode                = BindingMode.TwoWay,
//                     Source              = control.Value,
//                     UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
//                 };
// #else
//                 Binding binding = new("Value") {
//                     Mode = BindingMode.TwoWay,
//                     Source = control.Value,
//                     UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
//                 };
// #endif
//                 BindingOperations.SetBinding(obj, FrameworkElement.ToolTipProperty, binding);
//                 Canvas.SetLeft(obj, control.Value.X);
//                 Canvas.SetTop(obj, control.Value.Y);
//                 CanvasControl.Children.Add(obj);
//             }
//         }
//
//         // 第二次轮询进行变量初始化
//         foreach (var control in DescriptionHelper.Clock.ControlMap) {
//             control.Value.DisplayValue = control.Value.DefaultValue;
//             switch (control.Value.Type) {
//             case "RadioButton":
//                 if (control.Value.IsChecked) {
//                     DescriptionHelper.ChangeDefine(null, $"CSP_USING_{control.Value.Macro}", null);
//                 }
//
//                 break;
//             }
    //     }
    // }
}

// internal class ClockTreeViewModelTools
// {
//     public static TextBox CreateTextBox(ClockModel.ControlModel control) {
//         TextBox box = new() {
//             Width         = control.Width,
//             Height        = control.Height,
//             TextAlignment = TextAlignment.Center,
//             BorderBrush   = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#000000")!)
//         };
//
//         Binding binding = new("DisplayValue") {
//             Mode                = BindingMode.TwoWay,
//             Source              = control,
//             UpdateSourceTrigger = UpdateSourceTrigger.LostFocus
//         };
//         BindingOperations.SetBinding(box, TextBox.TextProperty, binding);
//
//         return box;
//     }
//
//     public static ComboBox CreateComboBox(ClockModel.ControlModel control) {
//         ComboBox box = new() {
//             Width                      = control.Width,
//             Height                     = control.Height,
//             HorizontalContentAlignment = HorizontalAlignment.Center,
//             BorderBrush                = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#000000")!)
//         };
//
//         Binding binding = new("Signals") {
//             Mode                = BindingMode.TwoWay,
//             Source              = control,
//             UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
//         };
//         BindingOperations.SetBinding(box, ComboBox.ItemsSourceProperty, binding);
//         box.DisplayMemberPath = "Text";
//         box.SelectedIndex     = control.DefaultIndex;
//
//         box.SelectionChanged += (sender, e) => {
//             string s = "";
//             foreach (var signal1 in control.Signals) {
//                 if (DescriptionHelper.IsDependence(signal1.DependenceArray)) {
//                     s = signal1.Source;
//                 }
//             }
//
//             if (box.SelectedItem is ClockModel.ControlModel.SignalModel signal2 && !s.IsNullOrEmpty()) {
//                 if (DescriptionHelper.Clock.ControlMap.ContainsKey(s)) {
//                     var ctrl = DescriptionHelper.Clock.ControlMap[s];
//                     control.Value = signal2.Operator.ToLower() switch {
//                         "/" => ctrl.Value / signal2.Value,
//                         "*" => ctrl.Value * signal2.Value,
//                         _   => control.Value
//                     };
//                 }
//             }
//         };
//
//         foreach (var ctl in DescriptionHelper.Clock.ControlMap) {
//             foreach (var signal1 in control.Signals) {
//                 if (ctl.Value.Name == signal1.Source && DescriptionHelper.IsDependence(signal1.DependenceArray)) {
//                     ctl.Value.PropertyChanged += (sender, e) => {
//                         string s = "";
//                         foreach (var signal2 in control.Signals) {
//                             if (DescriptionHelper.IsDependence(signal2.DependenceArray)) {
//                                 s = signal2.Source;
//                             }
//                         }
//
//                         if (box.SelectedItem is ClockModel.ControlModel.SignalModel signal3 && !s.IsNullOrEmpty()) {
//                             if (DescriptionHelper.Clock.ControlMap.ContainsKey(s)) {
//                                 var ctrl = DescriptionHelper.Clock.ControlMap[s];
//                                 control.Value = signal3.Operator.ToLower() switch {
//                                     "/" => ctrl.Value / signal3.Value,
//                                     "*" => ctrl.Value * signal3.Value,
//                                     _   => control.Value
//                                 };
//                             }
//                         }
//                     };
//                 }
//             }
//         }
//
//         return box;
//     }
//
//     public static TextBox CreateLabel(ClockModel.ControlModel control) {
//         TextBox box = new() {
//             Width                    = control.Width,
//             Height                   = control.Height,
//             TextAlignment            = TextAlignment.Center,
//             VerticalContentAlignment = VerticalAlignment.Center,
//             BorderBrush              = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#000000")!),
//             Style                    = null,
//             IsReadOnly               = true
//         };
//
//         if (control.Multiple != 0) {
//             Binding binding = new("DisplayValue") {
//                 Mode                = BindingMode.TwoWay,
//                 Source              = control,
//                 UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged
//             };
//             BindingOperations.SetBinding(box, TextBox.TextProperty, binding);
//         }
//
//         SetLabelStatus(ref box, control);
//         DescriptionHelper.Defines.PropertyChanged += (sender, e) => {
//             SetLabelStatus(ref box, control);
//             foreach (var signal in control.Signals) {
//                 if (DescriptionHelper.IsDependence(signal.DependenceArray)) {
//                     float value = 0;
//                     if (!signal.Source.IsNullOrEmpty()) {
//                         if (DescriptionHelper.Clock.ControlMap.ContainsKey(signal.Source)) {
//                             var ctrl = DescriptionHelper.Clock.ControlMap[signal.Source];
//                             value = ctrl.Value;
//                         }
//                         //TODO 出现错误
//                     }
//                     else if (signal.SourceValue != 0) {
//                         value = signal.SourceValue;
//                     }
//
//                     //TODO 出现错误
//                     control.Value = signal.Operator.ToLower() switch {
//                         "/" => value / signal.Value,
//                         "*" => value * signal.Value,
//                         _   => control.Value
//                     };
//                 }
//             }
//         };
//
//         foreach (var ctl in DescriptionHelper.Clock.ControlMap) {
//             foreach (var signal in control.Signals) {
//                 if (ctl.Value.Name == signal.Source) {
//                     ctl.Value.PropertyChanged += (sender, e) => {
//                         if (DescriptionHelper.IsDependence(signal.DependenceArray)) {
//                             control.Value = signal.Operator.ToLower() switch {
//                                 "/" => ctl.Value.Value / signal.Value,
//                                 "*" => ctl.Value.Value * signal.Value,
//                                 _   => control.Value
//                             };
//                         }
//                     };
//                 }
//             }
//         }
//
//         return box;
//     }
//
//     private static void SetLabelStatus(ref TextBox label, ClockModel.ControlModel control) {
//         foreach (var status in control.Status) {
//             if (DescriptionHelper.IsDependence(status.DependenceArray)) {
//                 foreach (var style in status.Styles) {
//                     switch (style.Name) {
//                     case "Text":
//                         label.Text = style.Value;
//
//                         break;
//
//                     case "Style":
//                         SetLabelStyle(ref label, style.Value);
//
//                         break;
//                     }
//                 }
//             }
//         }
//     }
//
//     private static void SetLabelStyle(ref TextBox label, string style) {
//         label.Background = style switch {
//             "Disable" => new SolidColorBrush((Color)ColorConverter.ConvertFromString("#e7ddb8")!),
//             "Enable"  => new SolidColorBrush((Color)ColorConverter.ConvertFromString("#b0ce95")!),
//             _         => label.Background
//         };
//     }
//
//     public static Viewbox CreateRadioButton(ClockModel.ControlModel control) {
//         Viewbox box = new() {
//             Width  = control.Width,
//             Height = control.Height
//         };
//         RadioButton button = new() {
//             GroupName   = control.GroupName,
//             Tag         = control.Name,
//             BorderBrush = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#000000")!),
//             IsChecked   = control.IsChecked
//         };
//
//         DescriptionHelper.Defines.PropertyChanged += (sender, e) => { };
//
//         button.Checked += (sender, e) => {
//             if (sender is RadioButton { IsChecked: true } rb) {
//                 string groupName = rb.GroupName;
//                 string name      = rb.Tag.ToString();
//                 foreach (var ctrl in DescriptionHelper.Clock.ControlMap) {
//                     if (ctrl.Value.GroupName == groupName) {
//                         if (ctrl.Value.Name == name) {
//                             DescriptionHelper.ChangeDefine(null, $"CSP_USING_{ctrl.Value.Macro}", null);
//                         }
//                         else {
//                             DescriptionHelper.ChangeDefine($"CSP_USING_{ctrl.Value.Macro}", null, null);
//                         }
//                     }
//                 }
//             }
//         };
//
//         box.Child = button;
//
//         return box;
//     }
// }