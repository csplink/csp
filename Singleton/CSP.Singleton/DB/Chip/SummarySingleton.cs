using CSP.Models.DB.Chip;

namespace CSP.Singleton.DB.Chip;

public static class SummarySingleton
{
    private static readonly SummarySingletonInstance Instance = SummarySingletonInstance.Instance;

    public static SummaryModel Summary => Instance.Summary;


    public static bool Add(string path) {
        Instance.Summary = SummaryModel.Load(path);

        return Instance.Summary != null;
    }
}