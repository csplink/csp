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
// @file        DocumentModel.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System;
using System.Collections.ObjectModel;
using System.Windows.Media.Imaging;
using CSP.Resources;
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
        if (string.IsNullOrWhiteSpace(name)) {
            throw new ArgumentNullException(nameof(name));
        }

        Children = new ObservableCollection<DocumentModel>();

        Image = Icon.YellowFolder;
        Name  = name;
    }

    public DocumentModel(string name, string url) {
        if (string.IsNullOrWhiteSpace(url)) {
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