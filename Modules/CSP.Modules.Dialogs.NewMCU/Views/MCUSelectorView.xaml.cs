using CSP.Modules.Dialogs.NewMCU.Models;
using CSP.Utils;
using Syncfusion.UI.Xaml.TreeView;

namespace CSP.Modules.Dialogs.NewMCU.Views;

public partial class MCUSelectorView
{
    public MCUSelectorView() {
        InitializeComponent();
    }

    private void OnSelectionChanged(object sender, ItemSelectionChangedEventArgs e) {
        object item = TreeView.SelectedItem;

        if (item is not DocumentModel value) {
            return;
        }

        if (!string.IsNullOrWhiteSpace(value.Url)) {
            Util.OpenUrl(value.Url);
        }
    }
}