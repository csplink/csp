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
// @file        SolutionExplorerEvent.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Windows.Media.Imaging;
using CSP.Resources;
using Prism.Events;
using Prism.Mvvm;

namespace CSP.Events;

public class SolutionExplorerEvent : PubSubEvent<IEnumerable<SolutionExplorerEvent.Model>>
{
    public class Model : BindableBase
    {
        private ObservableCollection<Model> _children;

        private BitmapImage    _image;
        private string         _name;
        private string         _path;
        public  Action<string> CallBack;

        public Model() {
        }

        public Model(string path) {
            if (string.IsNullOrWhiteSpace(path)) {
                throw new ArgumentNullException(nameof(path));
            }

            Children = new ObservableCollection<Model>();

            FileInfo info = new(path);

            if ((info.Attributes & FileAttributes.Directory) != 0) {
                Image = Icon.YellowFolder;
            }
            else {
                Image = System.IO.Path.GetExtension(info.Name).ToLower() switch {
                    ".c"      => Icon.C,
                    ".dll"    => Icon.Setting,
                    ".log"    => Icon.Log,
                    ".xml"    => Icon.Xml,
                    ".json"   => Icon.Json,
                    ".lib"    => Icon.Lib,
                    ".cs"     => Icon.CSharp,
                    ".config" => Icon.Log,
                    _         => Icon.C
                };
            }

            Name = info.Name;
        }

        public ObservableCollection<Model> Children {
            get => _children;
            set => SetProperty(ref _children, value);
        }

        public BitmapImage Image {
            get => _image;
            set => SetProperty(ref _image, value);
        }

        public string Name {
            get => _name;
            set => SetProperty(ref _name, value);
        }

        public string Path {
            get => _path;
            set => SetProperty(ref _path, value);
        }
    }
}