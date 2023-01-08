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
// @file        MapModelTests.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System.Collections.Generic;
using System.IO;
using CSP.Models.DB;
using CSP.Models.HAL.Config;
using CSP.Resources;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Models.Tests.HAL.Config;

public class MapModelTests
{
#if DEBUG
    private readonly string _mode = "Debug";
#else
    private readonly string _mode = "Release";
#endif
    private readonly ITestOutputHelper _testOutputHelper;

    public MapModelTests(ITestOutputHelper testOutputHelper) {
        _testOutputHelper = testOutputHelper;
    }

    public void Dispose() {
        ConfigFile.Save();
    }

    [Fact]
    public void Load() {
        string   solutionDir = File.ReadAllLines("./SolutionDir.txt")[0];
        string   dir         = $"{solutionDir}/Apps/CSP.Apps.Dev/bin/{_mode}/net6.0-windows/csp_repo/packages";
        string[] dirs        = Directory.GetDirectories(dir);
        foreach (string d in dirs) {
            string[] files = Directory.GetFiles(d, "*.json");
            foreach (string file in files) {
                _testOutputHelper.WriteLine($"load file: {file}");
                PackageModel package = PackageModel.Load(file);
                foreach (string version in package.Versions.Keys) {
                    dir =
                        $"{solutionDir}/Apps/CSP.Apps.Dev/bin/{_mode}/net6.0-windows/csp_repo/repositories/{package.Category}/{package.Name}/{version}/config/map";
                    if (!Directory.Exists(dir)) {
                        continue;
                    }

                    string[] mapFiles = Directory.GetFiles(dir, "*.yml");
                    foreach (string mapFile in mapFiles) {
                        _testOutputHelper.WriteLine($"load file: {mapFile}");
                        MapModel map = MapModel.Load(mapFile);
                        Assert.False(map == null);
                        Assert.False(map.Groups == null);
                        Assert.False(map.Properties == null);

                        Assert.False(map.Groups.Count == 0);
                        Assert.False(map.Properties.Count == 0);

                        Dictionary<string, string> total = new();

                        foreach (var (groupName, group) in map.Groups) {
                            Assert.False(group == null);
                            Assert.False(string.IsNullOrWhiteSpace(groupName));
                            Assert.False(!group.Comment.ContainsKey("zh-cn"));
                            Assert.False(group.Values == null);
                            Assert.False(group.Values.Count == 0);

                            foreach (var (valueName, value) in group.Values) {
                                Assert.False(value == null);
                                Assert.False(string.IsNullOrWhiteSpace(valueName));
                                Assert.False(!value.Comment.ContainsKey("zh-cn"));
                                total.Add(valueName, value.Comment["zh-cn"]);
                            }
                        }

                        foreach (var (propertyName, property) in map.Properties) {
                            Assert.False(property == null);
                            Assert.False(string.IsNullOrWhiteSpace(propertyName));
                            Assert.False(!property.DisplayName.ContainsKey("zh-cn"));
                            Assert.False(!property.Description.ContainsKey("zh-cn"));
                            Assert.False(string.IsNullOrWhiteSpace(property.Category));
                        }

                        Assert.False(total.Count != map.Total.Count);
                        foreach (var (name, value) in total) {
                            Assert.False(!map.Total.ContainsKey(name));
                            Assert.False(map.Total[name] != value);
                        }

                        Assert.False(map.Properties.Count != map.Attributes.Count);
                    }
                }
            }
        }
    }
}