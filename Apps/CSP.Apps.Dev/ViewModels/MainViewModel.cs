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