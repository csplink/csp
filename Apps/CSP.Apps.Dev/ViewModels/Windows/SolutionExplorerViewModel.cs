using CSP.Events;
using CSP.Resources;
using Prism.Events;
using Prism.Mvvm;
using Prism.Regions;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;

namespace CSP.Apps.Dev.ViewModels.Windows
{
    public class SolutionExplorerViewModel : BindableBase, INavigationAware
    {
        #region INavigationAware

        public bool IsNavigationTarget(NavigationContext navigationContext) {
            return true;
        }

        public void OnNavigatedFrom(NavigationContext navigationContext) {
        }

        public void OnNavigatedTo(NavigationContext navigationContext) {
        }

        #endregion INavigationAware

        private ObservableCollection<SolutionExplorerEvent.Model> _directories = new();

        public SolutionExplorerViewModel(IEventAggregator eventAggregator) {
            eventAggregator.GetEvent<SolutionExplorerEvent>().Subscribe(OnSolutionExplorerReceive);

            var rootNode1 = new SolutionExplorerEvent.Model("解决方案") { Image = Icon.YellowFolder };

            InitDirectories("./", rootNode1);
            Directories.Add(rootNode1);
        }

        public ObservableCollection<SolutionExplorerEvent.Model> Directories {
            get => _directories;
            set => SetProperty(ref _directories, value);
        }

        private static void InitDirectories(string path, SolutionExplorerEvent.Model fileInfo) {
            DirectoryInfo d = new(path);
            FileSystemInfo[] fsInfos = d.GetFileSystemInfos();
            var directories = new List<FileSystemInfo>();
            var files = new List<FileSystemInfo>();

            foreach (FileSystemInfo fsInfo in fsInfos) {
                if (fsInfo is DirectoryInfo) //判断是否为文件夹
                {
                    directories.Add(fsInfo);
                }
                else {
                    files.Add(fsInfo);
                }
            }

            foreach (var directory in directories) {
                var info = new SolutionExplorerEvent.Model(directory.FullName);
                InitDirectories(directory.FullName, info);//递归调用
                fileInfo.Children.Add(info);
            }

            foreach (var file in files) {
                var info = new SolutionExplorerEvent.Model(file.FullName);
                fileInfo.Children.Add(info);
            }
        }

        private void OnSolutionExplorerReceive(IEnumerable<SolutionExplorerEvent.Model> infos) {
            foreach (var info in infos) {
                Directories[0].Children.Insert(0, info);
            }
        }
    }
}