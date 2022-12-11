using System.Windows;
using CSP.Modules.Pages.MCU.Enums;

namespace CSP.Modules.Pages.MCU.Components.Espressif;

public partial class Pin
{
    public static readonly DependencyProperty DirectionProperty = DependencyProperty.Register("Direction",
        typeof(DirectionEnum),
        typeof(Pin),
        new FrameworkPropertyMetadata(DirectionEnum.Top, OnDirectionChanged) { BindsTwoWayByDefault = true });

    public Pin() {
        InitializeComponent();
    }

    public DirectionEnum Direction {
        get => (DirectionEnum)GetValue(DirectionProperty);
        set => SetValue(DirectionProperty, value);
    }

    private static void OnDirectionChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        if (d is not Pin pin) {
            return;
        }

        if (e.NewValue is not DirectionEnum direction) {
            return;
        }

        pin.ContentTemplate = pin.Resources[$"Pin{direction.ToString()}"] as DataTemplate;
    }
}