using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Windows;
using System.Windows.Media.Imaging;
using CSP.Models.DB.Chip;
using CSP.Models.Interfaces;
using CSP.Modules.Dialogs.NewMCU.Models;
using CSP.Resources;
using CSP.Services;
using CSP.Services.Models;
using CSP.Utils;
using Prism.Commands;
using Prism.Mvvm;
using Prism.Services.Dialogs;

namespace CSP.Modules.Dialogs.NewMCU.ViewModels;

using repository_t =
    Dictionary<string, Dictionary<string, Dictionary<string, Dictionary<string, RepositoryModel.MCUModel>>>>;

public class MCUSelectorViewModel : BindableBase, IDialogWindowParameters
{
    private readonly DocumentModel                       _applicationsDocumentNode = new("应用手册");
    private readonly DocumentModel                       _dataSheetsDocumentNode   = new("数据手册");
    private readonly DocumentModel                       _errataDocumentNode       = new("勘误手册");
    private readonly DocumentModel                       _programsDocumentNode     = new("编程手册");
    private readonly DocumentModel                       _referencesDocumentNode   = new("参考手册");
    private          ObservableCollection<DocumentModel> _documents                = new();
    private          bool                                _isBusy;
    private          Style                               _markdownStyle = MdXaml.MarkdownStyle.Sasabune;
    private          SummaryModel                        _mcu;
    private          BitmapImage                         _packageBitmapImage;
    private          repository_t                        _repository;
    private          RepositoryModel.MCUModel            _selectedMCU;
    private          Visibility                          _tabControlVisibility = Visibility.Collapsed;

    public MCUSelectorViewModel() {
        IsBusy      = true;
        _repository = RepositoryModel.Load($"{IniFile.PathRepo}/db/chips/repository.yml");
        IsBusy      = false;
    }

    public ObservableCollection<DocumentModel> Documents {
        get => _documents;
        set => SetProperty(ref _documents, value);
    }

    public bool IsBusy {
        get => _isBusy;
        set => SetProperty(ref _isBusy, value);
    }

    public Style MarkdownStyle {
        get => _markdownStyle;
        set => SetProperty(ref _markdownStyle, value);
    }

    public SummaryModel MCU {
        get => _mcu;
        set {
            SetProperty(ref _mcu, value);
            TabControlVisibility = value == null ? Visibility.Collapsed : Visibility.Visible;
        }
    }

    public DelegateCommand OnNew =>
        new(() => {
            if (MCU == null) {
                MessageBoxUtil.Error("未选择MCU或无MCU支持包");
            }
            else {
                if (string.IsNullOrWhiteSpace(SelectedMCU.Name) || string.IsNullOrWhiteSpace(SelectedMCU.Company)) {
                    MessageBoxUtil.Error("数据库发生错误");
                }
                else {
                    ProjectModel project = new() {
                        Header  = "### csp, (C) csp",
                        Version = "0.0.0.0",
                        Target = new ProjectModel.TargetModel {
                            Type = "MCU",
                            MCU = new ProjectModel.TargetModel.MCUModel {
                                Company = SelectedMCU.Company,
                                Name    = SelectedMCU.Name
                            }
                        }
                    };

                    ProjectHelper.Project = project;

                    DialogResult result = new(ButtonResult.OK);
                    RequestClose?.Invoke(result);
                }
            }
        });

    public DelegateCommand<object> OnOpenUrl =>
        new(obj => {
            if (obj is not string url) {
                return;
            }

            Util.OpenUrl(url);
        });

    public BitmapImage PackageBitmapImage {
        get => _packageBitmapImage;
        set => SetProperty(ref _packageBitmapImage, value);
    }

    public repository_t Repository {
        get => _repository;
        set => SetProperty(ref _repository, value);
    }

    public RepositoryModel.MCUModel SelectedMCU {
        get => _selectedMCU;

        set {
            if (!SetProperty(ref _selectedMCU, value)) {
                return;
            }

            if (value == null) {
                MCU = null;

                return;
            }

            MCU = SummaryModel.Load(
                $"{IniFile.PathRepo}/db/chips/{value.Company.ToLower()}/{value.Name.ToLower()}.yml");

            try {
                Uri path = new(@"pack://application:,,,/CSP.Modules.Dialogs.NewMCU;component/Resources/Images/" +
                               value.Package + @".png");
                PackageBitmapImage = new BitmapImage(path);
            }
            catch {
                Uri path = new(@"pack://application:,,,/CSP.Apps.Dev;component/Resources/Images/logo.png");
                PackageBitmapImage = new BitmapImage(path);
            }

            LoadDocuments();
        }
    }

    public Visibility TabControlVisibility {
        get => _tabControlVisibility;
        set => SetProperty(ref _tabControlVisibility, value);
    }

    private void LoadDocuments() {
        Documents.Clear();
        _dataSheetsDocumentNode.Children.Clear();
        _referencesDocumentNode.Children.Clear();
        _programsDocumentNode.Children.Clear();
        _errataDocumentNode.Children.Clear();
        _applicationsDocumentNode.Children.Clear();

        // if (MCU.dataSheets != null) {
        //     foreach (var item in MCU.dataSheets) {
        //         _dataSheetsDocumentNode.Children.Add(new DocumentModel(item.Name, item.Url));
        //     }
        // }
        //
        // if (MCU.References != null) {
        //     foreach (var item in MCU.References) {
        //         _referencesDocumentNode.Children.Add(new DocumentModel(item.Name, item.Url));
        //     }
        // }
        //
        // if (MCU.Programs != null) {
        //     foreach (var item in MCU.Programs) {
        //         _programsDocumentNode.Children.Add(new DocumentModel(item.Name, item.Url));
        //     }
        // }
        //
        // if (MCU.Errata != null) {
        //     foreach (var item in MCU.Errata) {
        //         _errataDocumentNode.Children.Add(new DocumentModel(item.Name, item.Url));
        //     }
        // }
        //
        // if (MCU.Applications != null) {
        //     foreach (var item in MCU.Applications) {
        //         _applicationsDocumentNode.Children.Add(new DocumentModel(item.Name, item.Url));
        //     }
        // }

        Documents.Add(_dataSheetsDocumentNode);
        Documents.Add(_referencesDocumentNode);
        Documents.Add(_programsDocumentNode);
        Documents.Add(_errataDocumentNode);
        Documents.Add(_applicationsDocumentNode);
    }

    #region IDialogWindowParameters

    private WindowState _windowState = WindowState.Maximized;

    public event Action<IDialogResult> RequestClose;

    public double Height => 300;

    public double MinHeight => 600;

    public double MinWidth => 900;

    public bool ShowInTaskbar => false;

    public SizeToContent SizeToContent => SizeToContent.Manual;

    public string Title => "创建项目";

    public double Width => 900;

    public WindowState WindowState {
        get => _windowState;
        set => SetProperty(ref _windowState, value);
    }

    public bool CanCloseDialog() {
        return true;
    }

    public void OnDialogClosed() {
    }

    public void OnDialogOpened(IDialogParameters parameters) {
    }

    #endregion IDialogWindowParameters
}