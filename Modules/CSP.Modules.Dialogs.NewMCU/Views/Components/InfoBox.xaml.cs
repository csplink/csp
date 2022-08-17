using CSP.Database.Models.MCU;
using CSP.Utils.Extensions;
using System;
using System.Diagnostics;
using System.Globalization;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media.Imaging;

namespace CSP.Modules.Dialogs.NewMCU.Views.Components
{
    public partial class InfoBox
    {
        public static readonly DependencyProperty MCUProperty = DependencyProperty.Register("MCU",
            typeof(MCUModel),
            typeof(InfoBox),
            new FrameworkPropertyMetadata(null, OnMCUChanged) { BindsTwoWayByDefault = true });

        public InfoBox()
        {
            InitializeComponent();
        }

        public MCUModel MCU
        {
            get => (MCUModel)GetValue(MCUProperty);
            set => SetValue(MCUProperty, value);
        }

        private static void OnMCUChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
        {
            ((InfoBox)d).OnMCUValueChanged(e);
        }

        private void ButtonUrlOnClick(object sender, RoutedEventArgs e)
        {
            if (sender is not Button button)
                return;

            var url = button.Tag.ToString();
            if (url.IsNullOrEmpty()) return;

            if (url != null)
            {
                _ = Process.Start("explorer.exe", url);
            }
        }

        private void OnMCUValueChanged(DependencyPropertyChangedEventArgs e)
        {
            if (e.NewValue == null)
            {
                ButtonUrl.Content = "NULL";
                ButtonUrl.Tag = null;
                TextBlockCompany.Text = "NULL";
                TextBlockIntroduction.Text = "NULL";
                TextBlockPrice.Text = "NULL";
                TextBlock.Text = "NULL";
                Image.Source = null;
            }

            if (e.NewValue is not MCUModel value)
                return;

            if (value.Package.IsNullOrEmpty())
                return;

            ButtonUrl.Content = MCU.Name;
            ButtonUrl.Tag = MCU.Url;

            TextBlockCompany.Text = MCU.Company;
            TextBlockIntroduction.Text = MCU.Introduction;
            TextBlockPrice.Text = MCU.Price.ToString(CultureInfo.InvariantCulture);

            TextBlock.Text = value.Package;

            var path = new Uri(@"pack://application:,,,/CSP.Modules.Dialogs.NewMCU;component/Resources/Images/" + value.Package + @".png");
            Image.Source = new BitmapImage(path);
        }
    }
}