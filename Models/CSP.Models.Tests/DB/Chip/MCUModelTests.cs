using CSP.Models.DB.Chip;
using CSP.Resources;
using System.IO;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Models.Tests.DB.Chip
{
    public class MCUModelTests
    {
#if DEBUG
        private readonly string _mode = "Debug";
#else
        private readonly string _mode = "Release";
#endif
        private readonly ITestOutputHelper _testOutputHelper;

        public MCUModelTests(ITestOutputHelper testOutputHelper) {
            _testOutputHelper = testOutputHelper;
        }

        public void Dispose() {
            IniFile.Save();
        }

        [Fact]
        public void Load() {
            var solutionDir = File.ReadAllLines("./SolutionDir.txt")[0];
            var path = $"{solutionDir}/Apps/CSP.Apps.Dev/bin/{_mode}/net6.0-windows/csp_repo/db/chips/repository.yml";
            var repository = RepositoryModel.Load(path);
            foreach (var companyName in repository.Keys) {
                var dir = $"{solutionDir}/Apps/CSP.Apps.Dev/bin/{_mode}/net6.0-windows/csp_repo/db/chips/{companyName.ToLower()}";
                var files = Directory.GetFiles(dir, "*.yml");
                foreach (var file in files) {
                    var mcu = MCUModel.Load(file);
                    Assert.False(mcu == null);
                    Assert.False(string.IsNullOrEmpty(mcu.ClockTree));
                    Assert.False(string.IsNullOrEmpty(mcu.Company));
                    Assert.False(string.IsNullOrEmpty(mcu.HAL));
                    Assert.False(string.IsNullOrEmpty(mcu.Line));
                    Assert.False(string.IsNullOrEmpty(mcu.Name));
                    Assert.False(string.IsNullOrEmpty(mcu.Package));
                    Assert.False(string.IsNullOrEmpty(mcu.Series));

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

                    Assert.False(!mcu.CompanyUrl.ContainsKey("Chinese"));
                    Assert.False(!mcu.Illustrate.ContainsKey("Chinese"));
                    Assert.False(!mcu.Introduction.ContainsKey("Chinese"));
                    Assert.False(!mcu.Url.ContainsKey("Chinese"));

                    Assert.False(string.IsNullOrEmpty(mcu.CompanyUrl["Chinese"]));
                    Assert.False(string.IsNullOrEmpty(mcu.Illustrate["Chinese"]));
                    Assert.False(string.IsNullOrEmpty(mcu.Introduction["Chinese"]));
                    Assert.False(string.IsNullOrEmpty(mcu.Url["Chinese"]));

                    foreach (var (key, value) in mcu.Documents) {
                        Assert.False(string.IsNullOrEmpty(key));
                        Assert.False(value == null);
                        Assert.False(value.Length == 0);
                        foreach (var document in value) {
                            Assert.False(string.IsNullOrEmpty(document.Name));
                            Assert.False(document.Url == null);
                            Assert.False(document.Url.Count == 0);
                            Assert.False(!document.Url.ContainsKey("Chinese"));
                            Assert.False(string.IsNullOrEmpty(document.Url["Chinese"]));
                        }
                    }

                    foreach (var (key, value) in mcu.Modules) {
                        Assert.False(string.IsNullOrEmpty(key));
                        Assert.False(value == null);
                        Assert.False(value.Length == 0);
                        foreach (var module in value) {
                            Assert.False(string.IsNullOrEmpty(module.Name));
                            Assert.False(module.Description == null);
                            Assert.False(module.Description.Count == 0);
                            Assert.False(!module.Description.ContainsKey("Chinese"));
                        }
                    }
                }
            }
        }
    }
}