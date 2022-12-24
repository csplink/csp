using System.Collections.Generic;
using CSP.Models.HAL.Config;

namespace CSP.Singleton.HAL.Config;

public static class PinoutSingleton
{
    private static readonly PinoutSingletonInstance Instance = PinoutSingletonInstance.Instance;

    public static Dictionary<string, PinoutModel> Pinouts => Instance.Pinouts;

    public static bool Set(string path) {
        Instance.Pinouts = PinoutModel.Load(path);

        return Instance.Pinouts != null;
    }
}