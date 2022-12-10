using System;
using System.Collections.ObjectModel;
using System.Windows.Media.Imaging;
using CSP.Resources;
using CSP.Utils.Extensions;
using Prism.Mvvm;

namespace CSP.Modules.Dialogs.NewMCU.Models;

public class DocumentModel : BindableBase
{
    private ObservableCollection<DocumentModel> _children;

    private BitmapImage _image;
    private bool        _isExpanded;
    private string      _name;
    private string      _url;

    public DocumentModel() {
    }

    public DocumentModel(string name) {
        if (name.IsNullOrEmpty()) {
            throw new ArgumentNullException(nameof(name));
        }

        Children = new ObservableCollection<DocumentModel>();

        Image = Icon.YellowFolder;
        Name  = name;
    }

    public DocumentModel(string name, string url) {
        if (url.IsNullOrEmpty()) {
            throw new ArgumentNullException(nameof(url));
        }

        Children = new ObservableCollection<DocumentModel>();

        Image = url.ToLower().EndsWith(".pdf") ? Icon.Pdf : Icon.Lib;
        Name  = name;
        Url   = url;
    }

    public ObservableCollection<DocumentModel> Children {
        get => _children;
        set => SetProperty(ref _children, value);
    }

    public BitmapImage Image {
        get => _image;
        set => SetProperty(ref _image, value);
    }

    public bool IsExpanded {
        get => _isExpanded;

        set => SetProperty(ref _isExpanded, value);
    }

    public string Name {
        get => _name;
        set => SetProperty(ref _name, value);
    }

    public string Url {
        get => _url;
        set => SetProperty(ref _url, value);
    }
}