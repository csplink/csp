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
// @file        NetUtilTests.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-12     xqyjlj       initial version
//

using System;
using System.Threading.Tasks;
using CSP.Resources;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Utils.Tests;

public class NetUtilTests : IDisposable
{
    private readonly ITestOutputHelper _testOutputHelper;

    public NetUtilTests(ITestOutputHelper testOutputHelper) {
        _testOutputHelper = testOutputHelper;
    }

    public void Dispose() {
    }

    [Fact]
    public async Task Check() {
        bool result = await NetUtil.Check("https://csplink.top/");
        Assert.False(!result);
    }

    [Fact]
    public void Ping() {
        string[] array =
            Resource.UrlGit.Split("\n", StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
        Assert.False(array.Length <= 0);
        foreach (string url in array) {
            float result = NetUtil.Ping(url);
            _testOutputHelper.WriteLine($"ping {url} => {result} ms");
        }
    }
}
