using CSP.Modules.Dialogs.NewMCU.Models;
using CSP.Utils;
using CSP.Utils.Extensions;
using Syncfusion.UI.Xaml.TreeView;

namespace CSP.Modules.Dialogs.NewMCU.Views
{
    public partial class MCUSelectorView
    {
        public MCUSelectorView()
        {
            InitializeComponent();
        }

        private void OnSelectionChanged(object sender, ItemSelectionChangedEventArgs e)
        {
            var item = TreeView.SelectedItem;

            if (item is not DocumentModel value)
                return;

            if (!value.Url.IsNullOrEmpty())
                Util.OpenUrl(value.Url);
        }
    }
}