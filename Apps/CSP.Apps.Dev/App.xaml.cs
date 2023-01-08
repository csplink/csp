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
// @file        App.xaml.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System.Text;
using System.Windows;
using CSP.Apps.Dev.Views;
using CSP.Modules.Dialogs.NewMCU;
using CSP.Modules.Pages.MCU;
using CSP.Resources;
using Prism.Ioc;
using Prism.Modularity;
using Prism.Regions;
using Serilog;
using Syncfusion.Windows.Tools.Controls;

namespace CSP.Apps.Dev;

public partial class App
{
    protected override void ConfigureModuleCatalog(IModuleCatalog moduleCatalog) {
        base.ConfigureModuleCatalog(moduleCatalog);

        moduleCatalog.AddModule<CSPModule>();

        moduleCatalog.AddModule<NewMCUModule>();

        moduleCatalog.AddModule<MCUModule>();
    }

    protected override void ConfigureRegionAdapterMappings(RegionAdapterMappings regionAdapterMappings) {
        base.ConfigureRegionAdapterMappings(regionAdapterMappings);
        regionAdapterMappings.RegisterMapping(typeof(DockingManager),
            Container.Resolve<RegionAdapter.DockingManager.RegionAdapter>());
    }

    protected override Window CreateShell() {
        return Container.Resolve<MainView>();
    }

    protected override void RegisterTypes(IContainerRegistry containerRegistry) {
    }

    private void OnAppExit(object sender, ExitEventArgs e) {
        ConfigFile.Save();
        Log.CloseAndFlush();
    }

    private void OnAppStartup(object sender, StartupEventArgs e) {
        Log.Logger = new LoggerConfiguration()
            .MinimumLevel.Verbose()
            .WriteTo.Debug()
            .WriteTo.File(ConfigFile.PathLogFile, //文件保存路径
                outputTemplate:
                "[{Timestamp:yyyy-MM-dd HH:mm:ss}] [{Level:u3}] {Message:lj}{NewLine}{Exception}", //输出日期格式
                rollingInterval: RollingInterval.Day,                                              //日志按日保存
                rollOnFileSizeLimit: true,                                                         // 限制单个文件的最大长度
                encoding: Encoding.UTF8,                                                           // 文件字符编码
                retainedFileCountLimit: 10,                                                        // 最大保存文件数
                fileSizeLimitBytes: 10 * 1024)                                                     // 最大单个文件长度
            .CreateLogger();
    }
}