using System;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Resources.Tests;

public class IniFileTests : IDisposable
{
    private readonly ITestOutputHelper _testOutputHelper;

    public IniFileTests(ITestOutputHelper testOutputHelper) {
        _testOutputHelper = testOutputHelper;
    }

    public void Dispose() {
        IniFile.Save();
    }

    [Fact]
    public void Test() {
        IniFile.PathRepo = "./";
        Assert.False(IniFile.PathRepo != "./");
    }
}