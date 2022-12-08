using CSP.Utils;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Windows;

namespace CSP.Models.HAL.Config
{
    public class PinoutModel
    {
        public Dictionary<string, FunctionModel> Functions { get; set; }
        public int Position { get; set; }
        public string Type { get; set; }

        public static Dictionary<string, PinoutModel> Load(string path) {
            DebugUtil.Assert(!string.IsNullOrWhiteSpace(path), new ArgumentNullException(nameof(path)));

            if (!File.Exists(path))
                return null;

            var deserializer = new YamlDotNet.Serialization.Deserializer();

            Dictionary<string, PinoutModel> rtn;
            try {
                using (var reader = new StreamReader(path)) {
                    rtn = deserializer.Deserialize<Dictionary<string, PinoutModel>>(reader);
                }
            }
            catch (InvalidOperationException e) {
                MessageBox.Show(e.Message, "error", MessageBoxButton.OK, MessageBoxImage.Error);
                return null;
            }

            DebugUtil.Assert(rtn != null, new ArgumentNullException("Pinout.YAML"), "YAML deserialization failed");

            var rtnSort = from pair in rtn orderby pair.Value.Position select pair; // must be sorted by position
            rtn = rtnSort.ToDictionary(pair => pair.Key, pair => pair.Value);
            return rtn;
        }

        public class FunctionModel
        {
            public string Mode { get; set; }
            public string Type { get; set; }
        }
    }
}