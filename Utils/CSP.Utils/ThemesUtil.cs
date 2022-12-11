using System.Windows;
using System.Windows.Media;
using Syncfusion.SfSkinManager;
using Syncfusion.Themes.Office2019Colorful.WPF;

namespace CSP.Utils;

public static class ThemesUtil
{
    public static void SetThemes(DependencyObject window, string theme) {
        Office2019ColorfulThemeSettings themeSettings = new() {
            FontFamily      = new FontFamily("Segoe UI, 微软雅黑"),
            BodyAltFontSize = 12
        };
        SfSkinManager.RegisterThemeSettings(theme, themeSettings);
        SfSkinManager.SetTheme(window, new Theme { ThemeName = theme });
    }
}