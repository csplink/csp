using System;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Resources.Tests;

public class ConfigFileTests : IDisposable
{
    private readonly ITestOutputHelper _testOutputHelper;

    public ConfigFileTests(ITestOutputHelper testOutputHelper) {
        _testOutputHelper = testOutputHelper;
    }

    public void Dispose() {
        ConfigFile.Save();
    }

    [Fact]
    public void Test() {
        ConfigFile.PathRepo = "./";
        Assert.False(ConfigFile.PathRepo != "./");
    }
}