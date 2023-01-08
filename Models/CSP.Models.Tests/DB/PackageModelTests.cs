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
// @file        PackageModelTests.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System.IO;
using CSP.Models.DB;
using CSP.Resources;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Models.Tests.DB;

public class PackageModelTests
{
#if DEBUG
    private readonly string _mode = "Debug";
#else
    private readonly string _mode = "Release";
#endif
    private readonly ITestOutputHelper _testOutputHelper;

    public PackageModelTests(ITestOutputHelper testOutputHelper) {
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
                Assert.False(package == null);
                Assert.False(string.IsNullOrWhiteSpace(package.Category));
                Assert.False(string.IsNullOrWhiteSpace(package.Homepage));
                Assert.False(string.IsNullOrWhiteSpace(package.License));
                Assert.False(string.IsNullOrWhiteSpace(package.Name));
                Assert.False(string.IsNullOrWhiteSpace(package.Option));
                Assert.False(string.IsNullOrWhiteSpace(package.Readme));

                Assert.False(string.IsNullOrWhiteSpace(package.Rule));
                Assert.False(string.IsNullOrWhiteSpace(package.Target));

                Assert.False(package.Author == null);
                Assert.False(package.Description == null);
                Assert.False(package.Repositories == null);
                Assert.False(package.Keywords == null);
                Assert.False(package.Versions == null);


                Assert.False(string.IsNullOrWhiteSpace(package.Author.Name));
                Assert.False(string.IsNullOrWhiteSpace(package.Author.Email));
                Assert.False(string.IsNullOrWhiteSpace(package.Author.Github));

                Assert.False(!package.Description.ContainsKey("zh-cn"));
                Assert.False(package.Repositories.Length <= 0);
                Assert.False(package.Keywords.Length <= 0);
                Assert.False(package.Versions.Count <= 0);
            }
        }
    }
}