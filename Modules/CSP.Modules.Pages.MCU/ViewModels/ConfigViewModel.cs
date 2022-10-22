using CSP.Events;
using CSP.Modules.Pages.MCU.Tools;
using CSP.Modules.Pages.MCU.Views;
using CSP.Resources;
using CSP.Utils;
using Prism.Events;
using Prism.Mvvm;
using Prism.Regions;
using System;
using System.Collections.Generic;

namespace CSP.Modules.Pages.MCU.ViewModels
{
    public class ConfigViewModel : BindableBase
    {
        private readonly IEventAggregator _eventAggregator;
        private readonly IRegionManager _regionManager;
        private int _selectedIndex;

        public ConfigViewModel(IRegionManager regionManager, IEventAggregator eventAggregator) {
            _regionManager = regionManager;
            _eventAggregator = eventAggregator;

            DescriptionHelper.Load("Espressif", "ESP32_S3_WROOM_1_N4");

            AddModules();

            // 添加MCU视图窗口
            try {
                var name = $"CSP.Modules.Pages.MCU.Views.Components.Package.{DescriptionHelper.MCU.Package}View";
                var type = Type.GetType(name);
                if (type != null)
                    RegionUtil.RegisterViewWithRegion(regionManager, "Region.MCU.Config.MCUView", type);
                else
                    MessageBoxUtil.Error($"此封装不存在：{DescriptionHelper.MCU.Package}");
            }
            catch {
                MessageBoxUtil.Error($"此封装不存在：{DescriptionHelper.MCU.Package}");
            }

            RegionUtil.RegisterViewWithRegion(regionManager, "Region.MCU.Config.ClockView", typeof(ClockTreeView));// 添加时钟视图窗口
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
                                RegionUtil.RequestNavigate(_regionManager, "Region.MCU.Config.PropertyTableView", $"Page.MCU.Config.PropertyTableView.Clock");
                                break;
                            }
                    }
                }
            }
        }

        private void AddModules() {
            DebugUtil.Assert(DescriptionHelper.MCU.Modules != null, new ArgumentNullException(nameof(DescriptionHelper.MCU.Modules)));

            if (DescriptionHelper.MCU.Modules == null)
                return;

            var infoRoot = new SolutionExplorerEvent.Model("模组") { Image = Icon.BlocksAndArrows };
            foreach (var module in DescriptionHelper.MCU.Modules) {
                var infoModule = new SolutionExplorerEvent.Model(module.Name) { Image = Icon.BlockOne };
                infoModule.CallBack += value => {
                };
                foreach (var category in module.Categories) {
                    var infoCategory = new SolutionExplorerEvent.Model(category.Name) { Image = Icon.BlockTwo };
                    infoCategory.CallBack += value => {
                        RegionUtil.RequestNavigate(_regionManager, "Region.MCU.Config.PropertyTableView", $"Page.MCU.Config.PropertyTableView.{value}");
                    };
                    infoModule.Children.Add(infoCategory);
                }
                infoRoot.Children.Add(infoModule);
            }

            var list = new List<SolutionExplorerEvent.Model> { infoRoot };

            _eventAggregator.GetEvent<SolutionExplorerEvent>().Publish(list);
        }

        private void OnEventGenerate(string message) {
            if (message != "Events.Generate")
                return;

            // save();

            var mcu = DescriptionHelper.MCU;
            if (mcu == null)
                return;

            // var project_singleton = ProjectSingleton.get_instance();
            // var manager = project_singleton.manager;
            //
            // if (manager?.target == null)
            //     return;

            // GenerateService.Generate(mcu, "./test");
        }
    }
}