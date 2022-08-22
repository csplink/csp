using System.IO;

namespace CSP.Extras.BeforeBuild.Tool.Resources
{
    internal static class Icon
    {
        private const string IconDataTemplate =
 @"
        public static BitmapImage $Data
        {
            get => Instance.$Data;
        }
";

        private const string IconInstanceDataTemplate = "        internal readonly BitmapImage $Data = new(new Uri(@\"pack://application:,,,/CSP.Resources;component/Icon/$Data.png\"));\r\n";

        private const string IconInstanceTemplate =
        @"using System;
using System.Windows.Media.Imaging;

namespace CSP.Resources
{
    internal  class IconInstance
    {
$Data    }
}";

        private const string IconTemplate =
@"using System.Windows.Media.Imaging;

namespace CSP.Resources
{
    public static class Icon
    {
        private static readonly IconInstance Instance = new();
$Data
    }
}";

        public static void Init() {
            var solutionDir = File.ReadAllLines("./SolutionDir.txt")[0];
            var resourcesIconPath = $"{solutionDir}Resources/CSP.Resources/Icon.cs";
            var resourcesIconInstancePath = $"{solutionDir}Resources/CSP.Resources/IconInstance.cs";
            var resourcesIconDir = $"{solutionDir}Resources/CSP.Resources/Icon";

            var iconInstanceData = "";
            var iconData = "";

            DirectoryInfo d = new(resourcesIconDir);
            FileSystemInfo[] fsInfos = d.GetFileSystemInfos();
            foreach (var fsInfo in fsInfos) {
                if (fsInfo is not DirectoryInfo) {
                    var name = fsInfo.Name.Replace(".png", "");
                    iconInstanceData += IconInstanceDataTemplate.Replace("$Data", name);
                    iconData += IconDataTemplate.Replace("$Data", name);
                }
            }

            // Console.WriteLine($"write IconInstance: \n {iconInstanceData}");
            // Console.WriteLine($"write Icon: \n {iconData}");

            var iconInstance = IconInstanceTemplate.Replace("$Data", iconInstanceData);
            var icon = IconTemplate.Replace("$Data", iconData);

            File.WriteAllText(resourcesIconPath, icon);
            File.WriteAllText(resourcesIconInstancePath, iconInstance);
        }
    }
}