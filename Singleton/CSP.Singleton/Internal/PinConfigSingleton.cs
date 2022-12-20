using System;
using System.Collections.Generic;
using CSP.Models.HAL.Config;
using CSP.Models.Internal;
using CSP.Utils;

namespace CSP.Singleton.Internal;

public static class PinConfigSingleton
{
    private static readonly PinConfigSingletonInstance Instance = PinConfigSingletonInstance.Instance;

    public static Dictionary<string, PinConfigModel> PinConfigs => Instance.PinConfigs;

    private static void Add(string name) {
        if (!PinConfigs.ContainsKey(name)) {
            PinConfigs[name] = new PinConfigModel();
        }
    }

    public static void Add(string name, PinoutModel pinOut) {
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(name), new ArgumentNullException(nameof(name)), "name is null");
        DebugUtil.Assert(pinOut == null, new ArgumentNullException(nameof(pinOut)), "pinOut is null");
        Add(name);
        PinConfigs[name!].Name.String    = name;
        PinConfigs[name].Position.String = pinOut!.Position.ToString();
    }
}