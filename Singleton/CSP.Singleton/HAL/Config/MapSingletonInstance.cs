using System;
using System.Collections.Generic;
using CSP.Models.HAL.Config;

namespace CSP.Singleton.HAL.Config;

internal class MapSingletonInstance
{
    private static readonly Lazy<MapSingletonInstance> Lazy = new(static () => new MapSingletonInstance());

    private MapSingletonInstance() {
    }

    public static MapSingletonInstance Instance => Lazy.Value;

    public Dictionary<string, MapModel> Maps { get; } = new();
}