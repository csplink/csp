using CSP.Resources;
using CSP.Utils.Extensions;
using Prism.Events;
using Prism.Mvvm;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Windows.Media.Imaging;

namespace CSP.Events
{
    public class SolutionExplorerEvent : PubSubEvent<IEnumerable<SolutionExplorerEvent.Model>>
    {
        public class Model : BindableBase
        {
            public Action<string> CallBack;
            private ObservableCollection<Model> _children;

            private BitmapImage _image;
            private string _name;
            private string _path;

            public Model() {
            }

            public Model(string path) {
                if (path.IsNullOrEmpty())
                    throw new ArgumentNullException(nameof(path));

                Children = new ObservableCollection<Model>();

                var info = new FileInfo(path);

                if ((info.Attributes & FileAttributes.Directory) != 0) {
                    Image = Icon.YellowFolder;
                }
                else {
                    Image = System.IO.Path.GetExtension(info.Name).ToLower() switch {
                        ".c" => Icon.C,
                        ".dll" => Icon.Setting,
                        ".log" => Icon.Log,
                        ".xml" => Icon.Xml,
                        ".json" => Icon.Json,
                        ".lib" => Icon.Lib,
                        ".cs" => Icon.CSharp,
                        ".config" => Icon.Log,
                        _ => Icon.C
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
}