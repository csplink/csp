using CSP.Database;
using CSP.Database.Components;
using CSP.Database.Models.MCU;
using CSP.Events;
using CSP.Modules.Pages.MCU.Services.Generate;
using CSP.Resources;
using CSP.Utils;
using Prism.Events;
using Prism.Mvvm;
using Prism.Regions;
using Syncfusion.Windows.PropertyGrid;
using System;
using System.Collections.Generic;

namespace CSP.Modules.Pages.MCU.ViewModels
{
    public class PinConfigViewModel : BindableBase, INavigationAware
    {
        #region INavigationAware

        public bool IsNavigationTarget(NavigationContext navigationContext)
        {
            return false;
        }

        public void OnNavigatedFrom(NavigationContext navigationContext)
        {
        }

        public void OnNavigatedTo(NavigationContext navigationContext)
        {
        }

        #endregion INavigationAware

        private readonly IEventAggregator _eventAggregator;
        private readonly IRegionManager _regionManager;

        public PinConfigViewModel(IRegionManager regionManager, IEventAggregator eventAggregator)
        {
            _regionManager = regionManager;
            _eventAggregator = eventAggregator;

            MCUHelper.LoadMcu("STMicroelectronics", "STM32F401RETx");

            AddCustomEditor();
            AddModules();

            _eventAggregator.GetEvent<GenerateEvent>().Subscribe(OnEventGenerate);
        }

        private void AddCustomEditor()
        {
            CustomEditor editor = new()
            {
                Editor = new ValuePropertyGridComboEditor(),
                HasPropertyType = true,
                PropertyType = typeof(MapModel.EnumerateModel.ValuePropertyGridComboEditorModel)
            };
            _eventAggregator.GetEvent<CustomEditorEvent>().Publish(editor);
        }

        private void AddModules()
        {
            var infoRoot = new SolutionExplorerEvent.Model("模组") { Image = Icon.BlocksAndArrows, IsExpanded = true };

            DebugUtil.Assert(MCUHelper.MCU.Modules != null, new ArgumentNullException(nameof(MCUHelper.MCU.Modules)));

            // ReSharper disable once PossibleNullReferenceException
            foreach (var module in MCUHelper.MCU.Modules)
            {
                var infoModule = new SolutionExplorerEvent.Model(module.Name) { Image = Icon.BlockOne, IsExpanded = true };
                infoModule.CallBack += value =>
                {
                };
                foreach (var category in module.Categories)
                {
                    var infoCategory = new SolutionExplorerEvent.Model(category.Name) { Image = Icon.BlockTwo, IsExpanded = true };
                    infoCategory.CallBack += value =>
                    {
                        RegionUtil.RequestNavigate(_regionManager, "Region.MCU.PinConfig.MCUConfig", $"Page.MCU.PinConfig.MCUConfig.{value}");
                    };
                    infoModule.Children.Add(infoCategory);
                }
                infoRoot.Children.Add(infoModule);
            }

            var list = new List<SolutionExplorerEvent.Model> { infoRoot };

            _eventAggregator.GetEvent<SolutionExplorerEvent>().Publish(list);
        }

        private void OnEventGenerate(string message)
        {
            if (message != "Events.Generate")
                return;

            // save();

            var mcu = MCUHelper.MCU;
            if (mcu == null)
                return;

            // var project_singleton = ProjectSingleton.get_instance();
            // var manager = project_singleton.manager;
            //
            // if (manager?.target == null)
            //     return;

            GenerateService.Generate(mcu, "./test");
        }
    }
}