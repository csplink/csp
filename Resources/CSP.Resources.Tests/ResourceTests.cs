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
// @file        ResourceTests.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-11     xqyjlj       initial version
//

using System;
using System.Threading.Tasks;
using CSP.Utils;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Resources.Tests;

public class ResourceTests : IDisposable
{
    private readonly ITestOutputHelper _testOutputHelper;

    public ResourceTests(ITestOutputHelper testOutputHelper) {
        _testOutputHelper = testOutputHelper;
    }

    public void Dispose() {
        ConfigFile.Save();
    }

    [Fact]
    public async Task UrlGit() {
        string[] array =
            Resource.UrlGit.Split("\n", StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
        Assert.False(array.Length <= 0);
        foreach (string url in array) {
            bool result = await NetUtil.Check(url);
            _testOutputHelper.WriteLine($"check {url} => {result}");
            Assert.False(!result);
        }
    }
}