using CSP.Utils;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Windows;

namespace CSP.Models.HAL.Config
{
    public class MapModel
    {
        public Dictionary<string, GroupModel> Groups { get; set; }
        public Dictionary<string, PropertyModel> Properties { get; set; }
        public static MapModel Load(string path) {
            DebugUtil.Assert(!string.IsNullOrWhiteSpace(path), new ArgumentNullException(nameof(path)));

            if (!File.Exists(path))
                return null;

            var deserializer = new YamlDotNet.Serialization.Deserializer();

            MapModel rtn;
            try {
                using (var reader = new StreamReader(path)) {
                    rtn = deserializer.Deserialize<MapModel>(reader);
                }
            }
            catch (InvalidOperationException e) {
                MessageBox.Show(e.Message, "error", MessageBoxButton.OK, MessageBoxImage.Error);
                return null;
            }

            DebugUtil.Assert(rtn != null, new ArgumentNullException("Map.YAML"), "YAML deserialization failed");
            return rtn;
        }
        public class GroupModel
        {
            public Dictionary<string, string> Comment { get; set; }
            public Dictionary<string, ValueModel> Values { get; set; }
            public class ValueModel
            {
                public Dictionary<string, string> Comment { get; set; }
            }
        }

        public class PropertyModel
        {
            public Dictionary<string, string> DisplayName { get; set; }
            public Dictionary<string, string> Description { get; set; }
            public string Category { get; set; }
            public bool ReadOnly { get; set; }
        }
    }


}
