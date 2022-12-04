namespace CSP.Resources
{
    public static class IniFile
    {
        private static readonly IniFileInstance Ini = new();

        public static string PathGit {
            get => Ini.ReadKey("Path", "Git", Path.Git);
            set => Ini.AddKey("Path", "Git", value);
        }

        public static string PathLogFile {
            get => Ini.ReadKey("Path", "LogFile", Path.LogFile);
            set => Ini.AddKey("Path", "LogFile", value);
        }

        public static string PathRepo {
            get => Ini.ReadKey("Path", "Repo", Path.Repo);
            set => Ini.AddKey("Path", "Repo", value);
        }

        public static void Save() {
            Ini.Save();
        }
    }
}
