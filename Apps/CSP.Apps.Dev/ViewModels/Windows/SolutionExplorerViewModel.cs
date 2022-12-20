using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using CSP.Events;
using CSP.Resources;
using Prism.Events;
using Prism.Mvvm;
using Prism.Regions;

namespace CSP.Apps.Dev.ViewModels.Windows;

public class SolutionExplorerViewModel : BindableBase, INavigationAware
{
    private ObservableCollection<SolutionExplorerEvent.Model> _directories = new();

    public SolutionExplorerViewModel(IEventAggregator eventAggregator) {
        eventAggregator.GetEvent<SolutionExplorerEvent>().Subscribe(OnSolutionExplorerReceive);

        SolutionExplorerEvent.Model rootNode1 = new SolutionExplorerEvent.Model("解决方案") { Image = Icon.YellowFolder };

        InitDirectories("./", rootNode1);
        Directories.Add(rootNode1);
    }

    public ObservableCollection<SolutionExplorerEvent.Model> Directories {
        get => _directories;
        set => SetProperty(ref _directories, value);
    }

    private static void InitDirectories(string path, SolutionExplorerEvent.Model fileInfo) {
        DirectoryInfo        d           = new(path);
        FileSystemInfo[]     fsInfos     = d.GetFileSystemInfos();
        List<FileSystemInfo> directories = new List<FileSystemInfo>();
        List<FileSystemInfo> files       = new List<FileSystemInfo>();

        foreach (FileSystemInfo fsInfo in fsInfos) {
            if (fsInfo is DirectoryInfo) //判断是否为文件夹
            {
                directories.Add(fsInfo);
            }
            else {
                files.Add(fsInfo);
            }
        }

        foreach (FileSystemInfo directory in directories) {
            SolutionExplorerEvent.Model info = new SolutionExplorerEvent.Model(directory.FullName);
            InitDirectories(directory.FullName, info); //递归调用
            fileInfo.Children.Add(info);
        }

        foreach (FileSystemInfo file in files) {
            SolutionExplorerEvent.Model info = new SolutionExplorerEvent.Model(file.FullName);
            fileInfo.Children.Add(info);
        }
    }

    private void OnSolutionExplorerReceive(IEnumerable<SolutionExplorerEvent.Model> infos) {
        foreach (SolutionExplorerEvent.Model info in infos) {
            Directories[0].Children.Insert(0, info);
        }
    }

    #region INavigationAware

    public bool IsNavigationTarget(NavigationContext navigationContext) {
        return true;
    }

    public void OnNavigatedFrom(NavigationContext navigationContext) {
    }

    public void OnNavigatedTo(NavigationContext navigationContext) {
    }

    #endregion INavigationAware
}