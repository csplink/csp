namespace CSP.Resources;

public static class ConfigFile
{
    private static readonly ConfigFileInstance Config = new();

    public static string PathGit {
        get => Config.ReadKey("Path", "Git", Path.Git);
        set => Config.AddKey("Path", "Git", value);
    }

    public static string PathLogFile {
        get => Config.ReadKey("Path", "LogFile", Path.LogFile);
        set => Config.AddKey("Path", "LogFile", value);
    }

    public static string PathRepo {
        get => Config.ReadKey("Path", "Repo", Path.Repo);
        set => Config.AddKey("Path", "Repo", value);
    }

    public static void Save() {
        Config.Save();
    }
}