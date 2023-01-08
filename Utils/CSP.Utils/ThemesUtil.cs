// Licensed under the Apache License, Version 2.0 (the "License");
// You may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// Copyright (C) 2022-2023 xqyjlj<xqyjlj@126.com>
//
// @author      xqyjlj
// @file        ThemesUtil.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

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