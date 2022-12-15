using System;
using System.Collections.Generic;
using System.IO;
using System.Windows;
using CSP.Utils;
using YamlDotNet.Serialization;

namespace CSP.Models.HAL.Config;

using ip_t = Dictionary<string, Dictionary<string, string[]>>;

public class IPModel
{
    public static ip_t Load(string path) {
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(path), new ArgumentNullException(nameof(path)));

        if (!File.Exists(path)) {
            return null;
        }

        Deserializer deserializer = new();

        ip_t rtn;
        try {
            using (StreamReader reader = new(path)) {
                rtn = deserializer.Deserialize<ip_t>(reader);
            }
        }
        catch (InvalidOperationException e) {
            MessageBox.Show(e.Message, "error", MessageBoxButton.OK, MessageBoxImage.Error);

            return null;
        }

        DebugUtil.Assert(rtn != null, new ArgumentNullException("IP.YAML"), "YAML deserialization failed");

        return rtn;
    }
}