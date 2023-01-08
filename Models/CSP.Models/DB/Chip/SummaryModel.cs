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
// @file        SummaryModel.cs
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
using YamlDotNet.Serialization;

namespace CSP.Models.DB.Chip;

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

        if (!File.Exists(path)) {
            return null;
        }

        Deserializer deserializer = new();

        SummaryModel rtn;
        try {
            using (StreamReader reader = new(path)) {
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