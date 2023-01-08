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
// @file        MainViewModel.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using CSP.Events;
using CSP.Utils;
using Prism.Commands;
using Prism.Events;
using Prism.Mvvm;
using Prism.Regions;
using Prism.Services.Dialogs;

namespace CSP.Apps.Dev.ViewModels;

public class MainViewModel : BindableBase
{
    private readonly IDialogService   _dialogService;
    private readonly IEventAggregator _eventAggregator;
    private readonly IRegionManager   _regionManager;

    public MainViewModel(IRegionManager regionManager, IEventAggregator eventAggregator, IDialogService dialogService) {
        _regionManager   = regionManager;
        _eventAggregator = eventAggregator;
        _dialogService   = dialogService;
    }

    public DelegateCommand OnBuild => new(() => { });

    public DelegateCommand OnGenerate =>
        new(() => { _eventAggregator.GetEvent<GenerateEvent>().Publish("Events.Generate"); });

    public DelegateCommand OnNewMCU =>
        new(() => {
            DialogUtil.ShowModalDialog(_dialogService, "Dialog.NewMCU", null, result => { }, "DialogWindow");
        });

    public DelegateCommand OnSave => new(() => { _eventAggregator.GetEvent<SaveEvent>().Publish("Events.Save"); });

    public DelegateCommand OnWindowClosing =>
        new(() => { _eventAggregator.GetEvent<ClosingEvent>().Publish("Events.Closing.Window"); });

    public DelegateCommand OnWindowRendered =>
        new(() => {
            _eventAggregator.GetEvent<RenderedEvent>().Publish("Events.Rendered.Window");

            RegionUtil.RequestNavigate(_regionManager, "Region.Window.Document", "Page.Home");
            RegionUtil.RequestNavigate(_regionManager, "Region.Window.Document", "Page.MCU.Config");
        });
}