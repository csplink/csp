using Syncfusion.SfSkinManager;
using Syncfusion.Themes.MaterialLight.WPF;
using System.Windows;
using System.Windows.Media;

namespace CSP.Utils
{
    public static class ThemesUtil
    {
        public static void SetThemes(DependencyObject window, string theme)
        {
            MaterialLightThemeSettings materialLightThemeSettings = new()
            {
                FontFamily = new FontFamily("Segoe UI, 微软雅黑"),
                BodyAltFontSize = 12
            };
            SfSkinManager.RegisterThemeSettings(theme, materialLightThemeSettings);
            SfSkinManager.SetTheme(window, new Theme { ThemeName = theme });
        }
    }
}