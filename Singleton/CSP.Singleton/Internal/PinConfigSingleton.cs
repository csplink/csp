using System.Collections.Generic;
using CSP.Models.HAL.Config;
using CSP.Models.Internal;

namespace CSP.Singleton.Internal;

public static class PinConfigSingleton
{
    private static readonly PinConfigSingletonInstance Instance = PinConfigSingletonInstance.Instance;

    public static Dictionary<string, PinConfigModel> PinConfigs => Instance.PinConfigs;

    public static void Add(string name) {
        if (!PinConfigs.ContainsKey(name)) {
            PinConfigs[name] = new PinConfigModel();
        }
    }

    public static void Add(string name, PinoutModel pinOut) {
        Add(name);
        PinConfigs[name].Name.String     = name;
        PinConfigs[name].Position.String = pinOut.Position.ToString();
    }
}