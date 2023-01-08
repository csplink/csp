// Licensed under the Apache License, Version 2.0 (the "License");
// You may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// Copyright (C) 2022-2023 xqyjlj<xqyjlj@126.com>
//
// @author      xqyjlj
// @file        RepositoryModel.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System;
using System.Collections.Generic;
using System.IO;
using System.Windows;
using CSP.Utils;
using Prism.Mvvm;
using YamlDotNet.Serialization;

namespace CSP.Models.DB.Chip;

using repository_t =
    Dictionary<string, Dictionary<string, Dictionary<string, Dictionary<string, RepositoryModel.MCUModel>>>>;

public class RepositoryModel
{
    [YamlIgnore]
    public repository_t Content { get; set; }

    public static RepositoryModel Load(string path) {
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(path), new ArgumentNullException(nameof(path)));

        if (!File.Exists(path)) {
            return null;
        }

        Deserializer    deserializer = new();
        RepositoryModel rtn          = new();
        try {
            using (StreamReader reader = new(path)) {
                rtn.Content = deserializer.Deserialize<repository_t>(reader);
            }
        }
        catch (InvalidOperationException e) {
            MessageBox.Show(e.Message, "error", MessageBoxButton.OK, MessageBoxImage.Error);

            return null;
        }

        DebugUtil.Assert(rtn.Content != null, new ArgumentNullException("Repository.YAML"),
            "YAML deserialization failed");
        foreach (var (companyName, companies) in rtn.Content!) {
            foreach (var (seriesName, series) in companies) {
                foreach (var (lineName, lines) in series) {
                    foreach (var (mcuName, mcu) in lines) {
                        mcu.Company = companyName;
                        mcu.Series  = seriesName;
                        mcu.Line    = lineName;
                        mcu.Name    = mcuName;
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