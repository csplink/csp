using System.Windows;
using System.Windows.Controls;

namespace CSP.Components
{
    public class DockControl : UserControl
    {
        public static readonly DependencyProperty IconProperty = DependencyProperty.Register("Icon",
            typeof(Image),
            typeof(DockControl),
            new FrameworkPropertyMetadata(null, OnIconChanged) { BindsTwoWayByDefault = true });

        public static readonly DependencyProperty KeyProperty = DependencyProperty.Register("Key",
            typeof(char),
            typeof(DockControl),
            new FrameworkPropertyMetadata('a', OnKeyChanged) { BindsTwoWayByDefault = true });

        public DockControl() {
        }

        public Image Icon {
            get => (Image)GetValue(IconProperty);
            set => SetValue(IconProperty, value);
        }

        public char Key {
            get => (char)GetValue(KeyProperty);
            set => SetValue(KeyProperty, value);
        }

        private static void OnIconChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        }

        private static void OnKeyChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) {
        }
    }
}