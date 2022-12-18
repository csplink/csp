using System;
using System.Collections.Generic;

namespace CSP.Singleton.HAL.Config;

using ip_t = Dictionary<string, Dictionary<string, string[]>>;

internal class IPSingletonInstance
{
    private static readonly Lazy<IPSingletonInstance> Lazy = new(static () => new IPSingletonInstance());

    private IPSingletonInstance() {
    }

    public static IPSingletonInstance Instance => Lazy.Value;

    public Dictionary<string, ip_t> IP { get; set; }
}