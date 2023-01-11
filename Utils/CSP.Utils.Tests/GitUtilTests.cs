using Xunit;
using Xunit.Abstractions;

namespace CSP.Utils.Tests;

public class GitUtilTests
{
    private readonly ITestOutputHelper _testOutputHelper;

    public GitUtilTests(ITestOutputHelper testOutputHelper) {
        _testOutputHelper = testOutputHelper;
    }

    public void Dispose() {
    }

    [Fact]
    public void GetGitVersionTest() {
        string version = GitUtil.GetGitVersion();
        _testOutputHelper.WriteLine(version);
        Assert.False(string.IsNullOrWhiteSpace(version));
    }
}