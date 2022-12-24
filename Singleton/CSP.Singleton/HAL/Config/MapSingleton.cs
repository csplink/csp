using System;
using System.Collections.Generic;
using System.IO;
using CSP.Models.HAL.Config;
using CSP.Utils;

namespace CSP.Singleton.HAL.Config;

public static class MapSingleton
{
    private static readonly MapSingletonInstance Instance = MapSingletonInstance.Instance;

    public static Dictionary<string, MapModel> Maps => Instance.Maps;

    public static bool Add(string path) {
        DebugUtil.Assert(File.Exists(path), new FileNotFoundException(path, $"{path} is not exists"));

        string name = Path.GetFileNameWithoutExtension(path);
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(name), new NullReferenceException(nameof(name)),
            $"{nameof(name)} is null or white space!");

        name = name!.ToLower();
        MapModel map = MapModel.Load(path);
        Instance.Maps.Add(name, map);

        return Instance.Maps.Count == 0 && Instance.Maps.ContainsKey(name);
    }

    public static bool Add(string name, MapModel map) {
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(name), new NullReferenceException(nameof(name)),
            $"{nameof(name)} is null or white space!");
        DebugUtil.Assert(map != null, new NullReferenceException(nameof(map)),
            $"{nameof(map)} is null!");

        Instance.Maps.Add(name!.ToLower(), map);

        return Instance.Maps.Count == 0 && Instance.Maps.ContainsKey(name);
    }
}