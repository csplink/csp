using CSP.Utils;
using System;
using System.Collections.Generic;
using System.IO;
using System.Windows;

namespace CSP.Models.DB.Chip
{
    public class SummaryModel
    {
        public string ClockTree { get; set; }
        public string Company { get; set; }
        public Dictionary<string, string> CompanyUrl { get; set; }
        public Dictionary<string, Dictionary<string, DocumentModel>> Documents { get; set; }
        public string HAL { get; set; }
        public bool HasPowerPad { get; set; }
        public Dictionary<string, string> Illustrate { get; set; }
        public Dictionary<string, string> Introduction { get; set; }
        public string Line { get; set; }
        public Dictionary<string, Dictionary<string, ModuleModel>> Modules { get; set; }
        public string Name { get; set; }
        public string Package { get; set; }
        public float Price { get; set; }
        public string Series { get; set; }
        public Dictionary<string, string> Url { get; set; }

        public static SummaryModel Load(string path) {
            DebugUtil.Assert(!string.IsNullOrWhiteSpace(path), new ArgumentNullException(nameof(path)));

            if (!File.Exists(path))
                return null;

            var deserializer = new YamlDotNet.Serialization.Deserializer();

            SummaryModel rtn;
            try {
                using (var reader = new StreamReader(path)) {
                    rtn = deserializer.Deserialize<SummaryModel>(reader);
                }
            }
            catch (InvalidOperationException e) {
                MessageBox.Show(e.Message, "error", MessageBoxButton.OK, MessageBoxImage.Error);
                return null;
            }

            DebugUtil.Assert(rtn != null, new ArgumentNullException("Summary.YAML"), "YAML deserialization failed");
            return rtn;
        }

        public class DocumentModel
        {
            public Dictionary<string, string> Url { get; set; }
        }

        public class ModuleModel
        {
            public Dictionary<string, string> Description { get; set; }
        }
    }
}