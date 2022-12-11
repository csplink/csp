using CSP.Events;
using Syncfusion.UI.Xaml.TreeView;

namespace CSP.Modules.Pages.MCU.Views.Components.Config;

public partial class GPIOView
{
    public GPIOView() {
        InitializeComponent();
    }

    private void OnSelectionChanged(object sender, ItemSelectionChangedEventArgs e) {
        object item = TreeView.SelectedItem;

        if (item is not SolutionExplorerEvent.Model value) {
            return;
        }

        value.CallBack?.Invoke(value.Name);
    }
}