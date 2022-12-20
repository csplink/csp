using System;
using CSP.Models.HAL.Config;

namespace CSP.Singleton.HAL.Config;

internal class ClockSingletonInstance
{
    private static readonly Lazy<ClockSingletonInstance> Lazy = new(static () => new ClockSingletonInstance());

    private ClockSingletonInstance() {
    }

    public static ClockSingletonInstance Instance => Lazy.Value;

    public ClockModel Clock { get; set; }
}