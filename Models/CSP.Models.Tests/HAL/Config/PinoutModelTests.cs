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
// @file        PinoutModelTests.cs
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

public class PinoutModelTests
{
#if DEBUG
    private readonly string _mode = "Debug";
#else
    private readonly string _mode = "Release";
#endif
    private readonly ITestOutputHelper _testOutputHelper;

    public PinoutModelTests(ITestOutputHelper testOutputHelper) {
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
                        $"{solutionDir}/Apps/CSP.Apps.Dev/bin/{_mode}/net6.0-windows/csp_repo/repositories/{package.Category}/{package.Name}/{version}/config";
                    if (!Directory.Exists(dir)) {
                        continue;
                    }

                    string[] configDirs = Directory.GetDirectories(dir);
                    foreach (string configDir in configDirs) {
                        string pinoutPath = $"{configDir}/pinout.yml";
                        if (!File.Exists(pinoutPath)) {
                            continue;
                        }

                        _testOutputHelper.WriteLine($"load file: {pinoutPath}");
                        Dictionary<string, PinoutModel> pinouts = PinoutModel.Load(pinoutPath);
                        Assert.False(pinouts == null);
                        int position = 0; // must be sorted by position
                        foreach (var (pinName, pinout) in pinouts) {
                            Assert.False(pinout == null);
                            Assert.False(string.IsNullOrWhiteSpace(pinName));
                            Assert.False(string.IsNullOrWhiteSpace(pinout.Type));
                            Assert.False(position >= pinout.Position);

                            position = pinout.Position;
                        }
                    }
                }
            }
        }
    }
}