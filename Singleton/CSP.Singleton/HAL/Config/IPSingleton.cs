﻿using System;
using System.Collections.Generic;
using System.IO;
using CSP.Models.HAL.Config;
using CSP.Utils;

namespace CSP.Singleton.HAL.Config;

public static class IPSingleton
{
    private static readonly IPSingletonInstance Instance = IPSingletonInstance.Instance;

    public static Dictionary<string, ip_t> IP => Instance.IP;

    public static bool Add(string path) {
        DebugUtil.Assert(File.Exists(path), new FileNotFoundException(path, $"{path} is not exists"));

        string name = Path.GetFileNameWithoutExtension(path);
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(name), new NullReferenceException(nameof(name)),
            $"{nameof(name)} is null or white space!");

        name = name!.ToUpper();
        ip_t ip = IPModel.Load(path).Content;
        Instance.IP.Add(name, ip);

        return Instance.IP.Count == 0 && Instance.IP.ContainsKey(name);
    }

    public static bool Add(string name, ip_t ip) {
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(name), new NullReferenceException(nameof(name)),
            $"{nameof(name)} is null or white space!");
        DebugUtil.Assert(ip != null, new NullReferenceException(nameof(ip)),
            $"{nameof(ip)} is null!");

        Instance.IP.Add(name!.ToUpper(), ip);

        return Instance.IP.Count == 0 && Instance.IP.ContainsKey(name);
    }
}