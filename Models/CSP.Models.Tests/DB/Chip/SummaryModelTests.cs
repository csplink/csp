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
// @file        SummaryModelTests.cs
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

public class SummaryModelTests
{
#if DEBUG
    private readonly string _mode = "Debug";
#else
    private readonly string _mode = "Release";
#endif
    private readonly ITestOutputHelper _testOutputHelper;

    public SummaryModelTests(ITestOutputHelper testOutputHelper) {
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
        foreach (string companyName in repository.Keys) {
            string dir =
                $"{solutionDir}/Apps/CSP.Apps.Dev/bin/{_mode}/net6.0-windows/csp_repo/db/chips/{companyName.ToLower()}";
            string[] files = Directory.GetFiles(dir, "*.yml");
            foreach (string file in files) {
                _testOutputHelper.WriteLine($"load file: {file}");
                SummaryModel mcu = SummaryModel.Load(file);
                Assert.False(mcu == null);
                Assert.False(string.IsNullOrWhiteSpace(mcu.ClockTree));
                Assert.False(string.IsNullOrWhiteSpace(mcu.Company));
                Assert.False(string.IsNullOrWhiteSpace(mcu.HAL));
                Assert.False(string.IsNullOrWhiteSpace(mcu.Line));
                Assert.False(string.IsNullOrWhiteSpace(mcu.Name));
                Assert.False(string.IsNullOrWhiteSpace(mcu.Package));
                Assert.False(string.IsNullOrWhiteSpace(mcu.Series));

                Assert.False(mcu.CompanyUrl == null);
                Assert.False(mcu.Documents == null);
                Assert.False(mcu.Illustrate == null);
                Assert.False(mcu.Introduction == null);
                Assert.False(mcu.Modules == null);
                Assert.False(mcu.Url == null);

                Assert.False(mcu.CompanyUrl.Count == 0);
                Assert.False(mcu.Illustrate.Count == 0);
                Assert.False(mcu.Introduction.Count == 0);
                Assert.False(mcu.Url.Count == 0);

                Assert.False(!mcu.CompanyUrl.ContainsKey("zh-cn"));
                Assert.False(!mcu.Illustrate.ContainsKey("zh-cn"));
                Assert.False(!mcu.Introduction.ContainsKey("zh-cn"));
                Assert.False(!mcu.Url.ContainsKey("zh-cn"));

                Assert.False(string.IsNullOrWhiteSpace(mcu.CompanyUrl["zh-cn"]));
                Assert.False(string.IsNullOrWhiteSpace(mcu.Illustrate["zh-cn"]));
                Assert.False(string.IsNullOrWhiteSpace(mcu.Introduction["zh-cn"]));
                Assert.False(string.IsNullOrWhiteSpace(mcu.Url["zh-cn"]));

                foreach (var (documentType, documents) in mcu.Documents) {
                    Assert.False(string.IsNullOrWhiteSpace(documentType));
                    Assert.False(documents == null);
                    Assert.False(documents.Count == 0);
                    foreach (var (documentName, document) in documents) {
                        Assert.False(string.IsNullOrWhiteSpace(documentName));
                        Assert.False(document.Url == null);
                        Assert.False(document.Url.Count == 0);
                        Assert.False(!document.Url.ContainsKey("zh-cn"));
                        Assert.False(string.IsNullOrWhiteSpace(document.Url["zh-cn"]));
                    }
                }

                foreach (var (moduleType, modules) in mcu.Modules) {
                    Assert.False(string.IsNullOrWhiteSpace(moduleType));
                    Assert.False(modules == null);
                    Assert.False(modules.Count == 0);
                    foreach (var (moduleName, module) in modules) {
                        Assert.False(string.IsNullOrWhiteSpace(moduleName));
                        Assert.False(module.Description == null);
                        Assert.False(module.Description.Count == 0);
                        Assert.False(!module.Description.ContainsKey("zh-cn"));
                    }
                }
            }
        }
    }
}