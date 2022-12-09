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
        IniFile.Save();
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
                Assert.False(string.IsNullOrWhiteSpace(package.Repository));
                Assert.False(string.IsNullOrWhiteSpace(package.Rule));
                Assert.False(string.IsNullOrWhiteSpace(package.Target));

                Assert.False(package.Author == null);
                Assert.False(package.Description == null);
                Assert.False(package.Keywords == null);
                Assert.False(package.Versions == null);

                Assert.False(string.IsNullOrWhiteSpace(package.Author.Name));
                Assert.False(string.IsNullOrWhiteSpace(package.Author.Email));
                Assert.False(string.IsNullOrWhiteSpace(package.Author.Github));

                Assert.False(!package.Description.ContainsKey("Chinese"));
                Assert.False(package.Keywords.Length <= 0);
                Assert.False(package.Versions.Length <= 0);
            }
        }
    }
}