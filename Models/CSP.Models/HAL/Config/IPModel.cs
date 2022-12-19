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
    [YamlIgnore]
    public ip_t Content { get; set; }

    public static IPModel Load(string path) {
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(path), new ArgumentNullException(nameof(path)));

        if (!File.Exists(path)) {
            return null;
        }

        Deserializer deserializer = new();
        IPModel      rtn          = new();
        try {
            using (StreamReader reader = new(path)) {
                rtn.Content = deserializer.Deserialize<ip_t>(reader);
            }
        }
        catch (InvalidOperationException e) {
            MessageBox.Show(e.Message, "error", MessageBoxButton.OK, MessageBoxImage.Error);

            return null;
        }

        DebugUtil.Assert(rtn.Content != null, new ArgumentNullException("IP.YAML"), "YAML deserialization failed");

        return rtn;
    }
}