using CSP.Models.HAL.Config;

namespace CSP.Singleton.HAL.Config;

public static class ClockSingleton
{
    private static readonly ClockSingletonInstance Instance = ClockSingletonInstance.Instance;

    public static ClockModel Clock => Instance.Clock;

    public static bool Set(string path) {
        Instance.Clock = ClockModel.Load(path);

        return Instance.Clock != null;
    }
}