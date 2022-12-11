using System.Windows;
using Serilog;

namespace CSP.Utils;

public static class MessageBoxUtil
{
    public static void Error(string message) {
        Log.Error(message);
        MessageBox.Show(message, "错误", MessageBoxButton.YesNo, MessageBoxImage.Error);
    }
}