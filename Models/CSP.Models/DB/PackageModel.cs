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
// @file        PackageModel.cs
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
using Json.Net;

namespace CSP.Models.DB;

public class PackageModel
{
    public AuthorModel Author { get; set; }

    public string Category { get; set; }

    public Dictionary<string, string> Description { get; set; }

    public string Homepage { get; set; }

    public string[] Keywords { get; set; }

    public string License { get; set; }

    public string Name { get; set; }

    public string Option { get; set; }

    public string Readme { get; set; }

    public string[] Repositories { get; set; }

    public string Rule { get; set; }

    public string Target { get; set; }

    public Dictionary<string, string[]> Versions { get; set; }

    public static PackageModel Load(string path) {
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(path), new ArgumentNullException(nameof(path)));

        if (!File.Exists(path)) {
            return null;
        }

        PackageModel rtn;
        try {
            using (StreamReader reader = new(path)) {
                rtn = JsonNet.Deserialize<PackageModel>(reader, PropertyNameTransforms.TitleToCamelCase);
            }
        }
        catch (InvalidOperationException e) {
            MessageBox.Show(e.Message, "error", MessageBoxButton.OK, MessageBoxImage.Error);

            return null;
        }

        DebugUtil.Assert(rtn != null, new ArgumentNullException("Package.JSON"), "JSON deserialization failed");

        if (!rtn!.Versions.ContainsKey("latest")) {
            rtn.Versions.Add("latest", null);
        }

        return rtn;
    }

    public class AuthorModel
    {
        public string Email { get; set; }

        public string Github { get; set; }

        public string Name { get; set; }
    }
}