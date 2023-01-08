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
// @file        RepositoryModelTests.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System.Collections.Generic;
using System.IO;
using CSP.Models.DB.Chip;
using CSP.Resources;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Models.Tests.DB.Chip;

using repository_t =
    Dictionary<string, Dictionary<string, Dictionary<string, Dictionary<string, RepositoryModel.MCUModel>>>>;

public class RepositoryModelTests
{
#if DEBUG
    private readonly string _mode = "Debug";
#else
    private readonly string _mode = "Release";
#endif
    private readonly ITestOutputHelper _testOutputHelper;

    public RepositoryModelTests(ITestOutputHelper testOutputHelper) {
        _testOutputHelper = testOutputHelper;
    }

    public void Dispose() {
        ConfigFile.Save();
    }

    [Fact]
    public void Load() {
        string solutionDir = File.ReadAllLines("./SolutionDir.txt")[0];
        string path = $"{solutionDir}/Apps/CSP.Apps.Dev/bin/{_mode}/net6.0-windows/csp_repo/db/chips/repository.yml";
        _testOutputHelper.WriteLine($"load file: {path}");
        repository_t repository = RepositoryModel.Load(path).Content;
        foreach (var (companyName, companies) in repository) {
            Assert.False(string.IsNullOrWhiteSpace(companyName));
            Assert.False(companies == null);
            foreach (var (seriesName, series) in companies) {
                Assert.False(string.IsNullOrWhiteSpace(seriesName));
                Assert.False(series == null);
                foreach (var (lineName, lines) in series) {
                    Assert.False(string.IsNullOrWhiteSpace(lineName));
                    Assert.False(lines == null);
                    foreach (var (mcuName, mcu) in lines) {
                        Assert.False(string.IsNullOrWhiteSpace(mcuName));
                        Assert.False(mcu == null);

                        Assert.False(string.IsNullOrWhiteSpace(mcu.Company));
                        Assert.False(string.IsNullOrWhiteSpace(mcu.Series));
                        Assert.False(string.IsNullOrWhiteSpace(mcu.Line));
                        Assert.False(string.IsNullOrWhiteSpace(mcu.Name));
                        Assert.False(string.IsNullOrWhiteSpace(mcu.Core));
                        Assert.False(string.IsNullOrWhiteSpace(mcu.Package));

                        Assert.False(mcu.Current == null);
                        Assert.False(mcu.Peripherals == null);
                        Assert.False(mcu.Temperature == null);
                        Assert.False(mcu.Voltage == null);

                        Assert.False(mcu.Peripherals.Count == 0);

                        Assert.False(mcu.Flash <= 0);
                        Assert.False(mcu.Frequency <= 0);
                        Assert.False(mcu.IO <= 0);
                        Assert.False(mcu.Ram <= 0);

                        Assert.False(mcu.Current.Lowest <= 0);
                        Assert.False(mcu.Current.Run <= 0);
                        Assert.False(mcu.Temperature.Max <= 0);
                        Assert.False(mcu.Voltage.Max <= 0);

                        foreach (var (peripheralName, peripheralCount) in mcu.Peripherals) {
                            Assert.False(string.IsNullOrWhiteSpace(peripheralName));
                            Assert.False(peripheralCount <= 0);
                        }
                    }
                }
            }
        }
    }
}