using System;
using System.Collections.Generic;
using CSP.Models.HAL.Config;

namespace CSP.Singleton.HAL.Config;

internal class PinoutSingletonInstance
{
    private static readonly Lazy<PinoutSingletonInstance> Lazy = new(static () => new PinoutSingletonInstance());

    private PinoutSingletonInstance() {
    }

    public static PinoutSingletonInstance Instance => Lazy.Value;

    public Dictionary<string, PinoutModel> Pinouts { get; set; }
}