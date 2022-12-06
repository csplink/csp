﻿using CSP.Utils;
using System;
using System.Collections.Generic;
using System.IO;
using System.Windows;

namespace CSP.Models.DB.Chip
{
    public class MCUModel
    {
        public string ClockTree { get; set; }
        public string Company { get; set; }
        public Dictionary<string, string> CompanyUrl { get; set; }
        public Dictionary<string, DocumentModel[]> Documents { get; set; }
        public string HAL { get; set; }
        public bool HasPowerPad { get; set; }
        public Dictionary<string, string> Illustrate { get; set; }
        public Dictionary<string, string> Introduction { get; set; }
        public string Line { get; set; }
        public Dictionary<string, ModuleModel[]> Modules { get; set; }
        public string Name { get; set; }
        public string Package { get; set; }
        public float Price { get; set; }
        public string Series { get; set; }
        public Dictionary<string, string> Url { get; set; }

        public static MCUModel Load(string path) {
            DebugUtil.Assert(!string.IsNullOrEmpty(path), new ArgumentNullException(nameof(path)));

            if (!File.Exists(path))
                return null;

            var deserializer = new YamlDotNet.Serialization.Deserializer();

            MCUModel rtn;
            try {
                using (var reader = new StreamReader(path)) {
                    rtn = deserializer.Deserialize<MCUModel>(reader);
                }
            }
            catch (InvalidOperationException e) {
                MessageBox.Show(e.Message, "error", MessageBoxButton.OK, MessageBoxImage.Error);
                return null;
            }

            DebugUtil.Assert(rtn != null, new ArgumentNullException("MCU.YAML"), "YAML deserialization failed");
            return rtn;
        }

        public class DocumentModel
        {
            public string Name { get; set; }
            public Dictionary<string, string> Url { get; set; }
        }

        public class ModuleModel
        {
            public Dictionary<string, string> Description { get; set; }
            public string Name { get; set; }
        }
    }
}