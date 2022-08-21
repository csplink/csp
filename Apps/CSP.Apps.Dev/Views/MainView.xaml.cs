using CSP.Utils;
using System.Globalization;

namespace CSP.Apps.Dev.Views
{
    public partial class MainView
    {
        public MainView()
        {
            System.Threading.Thread.CurrentThread.CurrentUICulture = new CultureInfo("zh-Hans");
            ThemesUtil.SetThemes(this, "Office2019Colorful");
            InitializeComponent();
        }

        // private void OnDockingManagerMainChildrenCollectionChanged(object sender, NotifyCollectionChangedEventArgs e)
        // {
        //     MenuView.Items.Clear();
        //     MenuView.Items.Add(new MenuItem { Header = "打开方式(_N)" });
        //     MenuView.Items.Add(new Separator());
        //     foreach (var child in DockingManagerMain.Children)
        //     {
        //         if (child is not DockControlModel dock)
        //             return;
        //
        //         var headerObj = DockingManager.GetHeader(dock);
        //
        //         if (headerObj is not string header)
        //             return;
        //
        //         if (dock.Key >= 'A' && dock.Key <= 'Z')
        //         {
        //             header = $"{header}(_{dock.Key})";
        //         }
        //
        //         MenuView.Items.Add(new MenuItem { Header = header, Icon = dock.Icon });
        //     }
        // }
    }
}