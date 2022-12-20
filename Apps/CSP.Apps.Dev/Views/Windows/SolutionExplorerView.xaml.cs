using System.Windows.Input;
using CSP.Events;

namespace CSP.Apps.Dev.Views.Windows;

public partial class SolutionExplorerView
{
    public SolutionExplorerView() {
        InitializeComponent();
    }

    private void OnPreviewMouseLeftButtonUp(object sender, MouseButtonEventArgs e) {
        object item = TreeView.SelectedItem;

        if (item is not SolutionExplorerEvent.Model value) {
            return;
        }

        value.CallBack?.Invoke(value.Name);
    }
}