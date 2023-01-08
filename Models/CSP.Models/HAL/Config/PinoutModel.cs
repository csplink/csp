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
// @file        PinoutModel.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Windows;
using CSP.Utils;
using YamlDotNet.Serialization;

namespace CSP.Models.HAL.Config;

public class PinoutModel
{
    public Dictionary<string, FunctionModel> Functions { get; set; }

    public int Position { get; set; }

    public string Type { get; set; }

    public static Dictionary<string, PinoutModel> Load(string path) {
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(path), new ArgumentNullException(nameof(path)));

        if (!File.Exists(path)) {
            return null;
        }

        Deserializer deserializer = new();

        Dictionary<string, PinoutModel> rtn;
        try {
            using (StreamReader reader = new(path)) {
                rtn = deserializer.Deserialize<Dictionary<string, PinoutModel>>(reader);
            }
        }
        catch (InvalidOperationException e) {
            MessageBox.Show(e.Message, "error", MessageBoxButton.OK, MessageBoxImage.Error);

            return null;
        }

        DebugUtil.Assert(rtn != null, new ArgumentNullException("Pinout.YAML"), "YAML deserialization failed");

        IOrderedEnumerable<KeyValuePair<string, PinoutModel>> rtnSort =
            from pair in rtn orderby pair.Value.Position select pair; // must be sorted by position
        rtn = rtnSort.ToDictionary(pair => pair.Key, pair => pair.Value);

        return rtn;
    }

    public class FunctionModel
    {
        public string Mode { get; set; }

        public string Type { get; set; }
    }
}