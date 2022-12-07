using CSP.Models.DB;
using CSP.Resources;
using System.IO;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Models.Tests.DB
{
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
            var solutionDir = File.ReadAllLines("./SolutionDir.txt")[0];
            var dir = $"{solutionDir}/Apps/CSP.Apps.Dev/bin/{_mode}/net6.0-windows/csp_repo/packages";
            var dirs = Directory.GetDirectories(dir);
            foreach (var d in dirs) {
                var files = Directory.GetFiles(d, "*.json");
                foreach (var file in files) {
                    var package = PackageModel.Load(file);
                    Assert.False(package == null);
                    Assert.False(string.IsNullOrEmpty(package.Category));
                    Assert.False(string.IsNullOrEmpty(package.Homepage));
                    Assert.False(string.IsNullOrEmpty(package.License));
                    Assert.False(string.IsNullOrEmpty(package.Name));
                    Assert.False(string.IsNullOrEmpty(package.Option));
                    Assert.False(string.IsNullOrEmpty(package.Readme));
                    Assert.False(string.IsNullOrEmpty(package.Repository));
                    Assert.False(string.IsNullOrEmpty(package.Rule));
                    Assert.False(string.IsNullOrEmpty(package.Target));

                    Assert.False(package.Author == null);
                    Assert.False(package.Description == null);
                    Assert.False(package.Keywords == null);
                    Assert.False(package.Versions == null);

                    Assert.False(string.IsNullOrEmpty(package.Author.Name));
                    Assert.False(string.IsNullOrEmpty(package.Author.Email));
                    Assert.False(string.IsNullOrEmpty(package.Author.Github));

                    Assert.False(!package.Description.ContainsKey("Chinese"));
                    Assert.False(package.Keywords.Length <= 0);
                    Assert.False(package.Versions.Length <= 0);
                }
            }
        }
    }
}