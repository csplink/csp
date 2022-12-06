using CSP.Utils;
using Prism.Mvvm;
using System;
using System.Collections.Generic;
using System.IO;
using System.Windows;

namespace CSP.Models.DB.Chip
{
    using repository_t = Dictionary<string, Dictionary<string, Dictionary<string, Dictionary<string, RepositoryModel.MCUModel>>>>;

    public class RepositoryModel
    {
        public static repository_t Load(string path) {
            DebugUtil.Assert(!string.IsNullOrEmpty(path), new ArgumentNullException(nameof(path)));

            if (!File.Exists(path))
                return null;

            var deserializer = new YamlDotNet.Serialization.Deserializer();

            repository_t rtn;
            try {
                using (var reader = new StreamReader(path)) {
                    rtn = deserializer.Deserialize<repository_t>(reader);
                }
            }
            catch (InvalidOperationException e) {
                MessageBox.Show(e.Message, "error", MessageBoxButton.OK, MessageBoxImage.Error);
                return null;
            }

            DebugUtil.Assert(rtn != null, new ArgumentNullException("Repository.YAML"), "YAML deserialization failed");

            if (rtn == null)
                return null;

            foreach (var (companyName, companies) in rtn) {
                foreach (var (seriesName, series) in companies) {
                    foreach (var (lineName, lines) in series) {
                        foreach (var (mcuName, mcu) in lines) {
                            mcu.Company = companyName;
                            mcu.Series = seriesName;
                            mcu.Line = lineName;
                            mcu.Name = mcuName;
                            //TODO Price list data updater needs to be added here
                        }
                    }
                }
            }
            return rtn;
        }

        public class MCUModel
        {
            public string Company { get; set; }
            public string Core { get; set; }
            public CurrentModel Current { get; set; }
            public float Flash { get; set; }
            public float Frequency { get; set; }
            public int IO { get; set; }
            public string Line { get; set; }
            public string Name { get; set; }
            public string Package { get; set; }
            public Dictionary<string, int> Peripherals { get; set; }
            public float Price { get; set; }
            public float Ram { get; set; }
            public string Series { get; set; }
            public TemperatureModel Temperature { get; set; }
            public VoltageModel Voltage { get; set; }

            public class CurrentModel
            {
                public float Lowest { get; set; }
                public float Run { get; set; }
            }

            public class TemperatureModel : BindableBase
            {
                public float Max { get; set; }
                public float Min { get; set; }
            }

            public class VoltageModel : BindableBase
            {
                public float Max { get; set; }
                public float Min { get; set; }
            }
        }
    }
}