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
// @file        MapModel.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Windows;
using CSP.Utils;
using YamlDotNet.Serialization;

namespace CSP.Models.HAL.Config;

public class MapModel
{
    public Dictionary<string, GroupModel> Groups { get; set; }

    [YamlIgnore]
    public ObservableDictionary<string, ObservableDictionary<string, Attribute>> Attributes { get; } = new();

    [YamlIgnore]
    public Dictionary<string, string> Total { get; } = new();

    public Dictionary<string, PropertyModel> Properties { get; set; }

    public static MapModel Load(string path) {
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(path), new ArgumentNullException(nameof(path)));

        if (!File.Exists(path)) {
            return null;
        }

        Deserializer deserializer = new();

        MapModel rtn;
        try {
            using (StreamReader reader = new(path)) {
                rtn = deserializer.Deserialize<MapModel>(reader);
            }
        }
        catch (InvalidOperationException e) {
            MessageBox.Show(e.Message, "error", MessageBoxButton.OK, MessageBoxImage.Error);

            return null;
        }

        DebugUtil.Assert(rtn != null, new ArgumentNullException("Map.YAML"), "YAML deserialization failed");

        foreach (var (_, group) in rtn!.Groups) {
            foreach (var (name, value) in group.Values) {
                rtn.Total.Add(name, value.Comment["zh-cn"]);
            }
        }

        foreach (var (propertyName, property) in rtn!.Properties) {
            ObservableDictionary<string, Attribute> attributes = new() {
                { "DisplayName", new DisplayNameAttribute(property.DisplayName["zh-cn"]) },
                { "Description", new DescriptionAttribute(property.Description["zh-cn"]) },
                { "Category", new CategoryAttribute(property.Category) },
                { "ReadOnly", new ReadOnlyAttribute(property.ReadOnly) }
            };
            rtn.Attributes.Add(propertyName, attributes);
        }

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