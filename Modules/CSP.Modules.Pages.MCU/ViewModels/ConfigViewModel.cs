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
// @file        ConfigViewModel.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System;
using System.Collections.Generic;
using System.IO;
using CSP.Events;
using CSP.Models.DB.Chip;
using CSP.Modules.Pages.MCU.Views;
using CSP.Resources;
using CSP.Singleton.DB;
using CSP.Singleton.DB.Chip;
using CSP.Singleton.HAL.Config;
using CSP.Singleton.Internal;
using CSP.Utils;
using Prism.Events;
using Prism.Mvvm;
using Prism.Regions;

namespace CSP.Modules.Pages.MCU.ViewModels;

public class ConfigViewModel : BindableBase
{
    private readonly IEventAggregator _eventAggregator;
    private readonly IRegionManager   _regionManager;
    private          int              _selectedIndex;

    public ConfigViewModel(IRegionManager regionManager, IEventAggregator eventAggregator) {
        _regionManager   = regionManager;
        _eventAggregator = eventAggregator;

        LoadMCU("geehy", "apm32f103zet6");

        AddModules();

        // 添加MCU视图窗口
        try {
            string name = $"CSP.Modules.Pages.MCU.Views.Components.Package.LQFP.{SummarySingleton.Summary.Package}View";
            Type   type = Type.GetType(name);
            if (type != null) {
                RegionUtil.RegisterViewWithRegion(regionManager, "Region.MCU.Config.MCUView", type);
            }
            else {
                MessageBoxUtil.Error($"此封装不存在：{SummarySingleton.Summary.Package}");
            }
        }
        catch {
            MessageBoxUtil.Error($"此封装不存在：{SummarySingleton.Summary.Package}");
        }

        RegionUtil.RegisterViewWithRegion(regionManager, "Region.MCU.Config.ClockView",
            typeof(ClockTreeView)); // 添加时钟视图窗口
        _eventAggregator.GetEvent<GenerateEvent>().Subscribe(OnEventGenerate);
    }

    public int SelectedIndex {
        get => _selectedIndex;
        set {
            if (SetProperty(ref _selectedIndex, value)) {
                switch (SelectedIndex) {
                case 0: {
                    break;
                }
                case 1: {
                    RegionUtil.RequestNavigate(_regionManager, "Region.MCU.Config.PropertyTableView",
                        "Page.MCU.Config.PropertyTableView.Clock");

                    break;
                }
                }
            }
        }
    }

    private void AddModules() {
        DebugUtil.Assert(SummarySingleton.Summary.Modules != null,
            new ArgumentNullException(nameof(SummarySingleton.Summary.Modules)));

        if (SummarySingleton.Summary.Modules == null) {
            return;
        }

        SolutionExplorerEvent.Model infoRoot = new("模组") { Image = Icon.BlocksAndArrows };
        foreach (var (moduleName, module) in SummarySingleton.Summary
                     .Modules) {
            SolutionExplorerEvent.Model infoModule = new(moduleName) {
                Image = Icon.BlockOne
            };
            infoModule.CallBack += value => { };
            foreach (var (categoryName, category) in module) {
                SolutionExplorerEvent.Model infoCategory = new(categoryName)
                    { Image = Icon.BlockTwo };
                infoCategory.CallBack += value => {
                    RegionUtil.RequestNavigate(_regionManager, "Region.MCU.Config.PropertyTableView",
                        $"Page.MCU.Config.PropertyTableView.{value}");
                };
                infoModule.Children.Add(infoCategory);
            }

            infoRoot.Children.Add(infoModule);
        }

        List<SolutionExplorerEvent.Model> list = new() { infoRoot };

        _eventAggregator.GetEvent<SolutionExplorerEvent>().Publish(list);
    }

    private void LoadMCU(string company, string name) {
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(company), new ArgumentNullException(nameof(company)));
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(name), new ArgumentNullException(nameof(name)));

        string summaryPath = $"{ConfigFile.PathRepo}/db/chips/{company!.ToLower()}/{name!.ToLower()}.yml";
        SummarySingleton.Set(summaryPath);
        DebugUtil.Assert(SummarySingleton.Summary != null, new ArgumentNullException(nameof(SummarySingleton.Summary)));

        string hal            = SummarySingleton.Summary!.HAL;
        string halPackagePath = $"{ConfigFile.PathRepo}/packages/hal/{hal}.json";
        PackageSingleton.Set(halPackagePath);
        DebugUtil.Assert(PackageSingleton.Package != null, new ArgumentNullException(nameof(PackageSingleton.Package)));

        IEnumerable<string> versions = PackageSingleton.Package!.Versions.Keys;
        string              version  = "latest"; // default use latest version

        string pinoutPath = $"{ConfigFile.PathRepo}/repositories/hal/{hal}/{version}/config/{name}/pinout.yml";
        PinoutSingleton.Set(pinoutPath);
        DebugUtil.Assert(PinoutSingleton.Pinouts != null, new ArgumentNullException(nameof(PinoutSingleton.Pinouts)));

        foreach (var (pinoutName, pinout) in PinoutSingleton.Pinouts!) {
            PinConfigSingleton.Add(pinoutName, pinout);
        }

        string   ipDir   = $"{ConfigFile.PathRepo}/repositories/hal/{hal}/{version}/config/{name}/ip";
        string[] ipFiles = Directory.GetFiles(ipDir, "*.yml");
        foreach (string ipFile in ipFiles) {
            IPSingleton.Add(ipFile);
        }

        string   mapDir   = $"{ConfigFile.PathRepo}/repositories/hal/{hal}/{version}/config/map";
        string[] mapFiles = Directory.GetFiles(mapDir, "*.yml");
        foreach (string mapFile in mapFiles) {
            MapSingleton.Add(mapFile);
        }

        string clockPath = $"{ConfigFile.PathRepo}/repositories/hal/{hal}/{version}/config/{name}/clock/{name}.yml";
        ClockSingleton.Set(clockPath);
    }

    private void OnEventGenerate(string message) {
        if (message != "Events.Generate") {
            return;
        }

        // save();

        SummaryModel mcu = SummarySingleton.Summary;

        if (mcu == null) {
            return;
        }

        // var project_singleton = ProjectSingleton.get_instance();
        // var manager = project_singleton.manager;
        //
        // if (manager?.target == null)
        //     return;

        // GenerateService.Generate(mcu, "./test");
    }
}