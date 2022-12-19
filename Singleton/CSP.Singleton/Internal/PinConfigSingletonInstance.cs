using System;
using System.Collections.Generic;
using CSP.Models.Internal;

namespace CSP.Singleton.Internal;

internal class PinConfigSingletonInstance
{
    private static readonly Lazy<PinConfigSingletonInstance> Lazy = new(static () => new PinConfigSingletonInstance());

    private PinConfigSingletonInstance() {
    }

    public static PinConfigSingletonInstance Instance => Lazy.Value;

    public Dictionary<string, PinConfigModel> PinConfigs { get; } = new();
}