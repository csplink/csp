﻿using System;
using System.Collections.Generic;
using CSP.Events;
using CSP.Models.DB.Chip;
using CSP.Modules.Pages.MCU.Views;
using CSP.Resources;
using CSP.Singleton.DB.Chip;
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

        // DescriptionHelper.Load("Geehy", "APM32F103ZET6");

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