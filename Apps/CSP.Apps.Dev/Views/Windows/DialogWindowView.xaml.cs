using CSP.Utils;
using Prism.Services.Dialogs;

namespace CSP.Apps.Dev.Views.Windows;

public partial class DialogWindowView : IDialogWindow
{
    public DialogWindowView() {
        ThemesUtil.SetThemes(this, "Office2019Colorful");

        InitializeComponent();
    }

    public IDialogResult Result { get; set; }
}