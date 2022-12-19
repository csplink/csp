global using ip_t =
    System.Collections.Generic.Dictionary<string, System.Collections.Generic.Dictionary<string, string[]>>;
using System;
using System.Collections.Generic;

namespace CSP.Singleton.HAL.Config;

internal class IPSingletonInstance
{
    private static readonly Lazy<IPSingletonInstance> Lazy = new(static () => new IPSingletonInstance());

    private IPSingletonInstance() {
    }

    public static IPSingletonInstance Instance => Lazy.Value;

    public Dictionary<string, ip_t> IP { get; set; }
}