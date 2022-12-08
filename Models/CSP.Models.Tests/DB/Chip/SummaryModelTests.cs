using CSP.Models.DB.Chip;
using CSP.Resources;
using System.IO;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Models.Tests.DB.Chip
{
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
            IniFile.Save();
        }

        [Fact]
        public void Load() {
            var solutionDir = File.ReadAllLines("./SolutionDir.txt")[0];
            var path = $"{solutionDir}/Apps/CSP.Apps.Dev/bin/{_mode}/net6.0-windows/csp_repo/db/chips/repository.yml";
            _testOutputHelper.WriteLine($"load file: {path}");
            var repository = RepositoryModel.Load(path);
            foreach (var companyName in repository.Keys) {
                var dir = $"{solutionDir}/Apps/CSP.Apps.Dev/bin/{_mode}/net6.0-windows/csp_repo/db/chips/{companyName.ToLower()}";
                var files = Directory.GetFiles(dir, "*.yml");
                foreach (var file in files) {
                    _testOutputHelper.WriteLine($"load file: {file}");
                    var mcu = SummaryModel.Load(file);
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

                    foreach (var (documentType, documents) in mcu.Documents) {
                        Assert.False(string.IsNullOrEmpty(documentType));
                        Assert.False(documents == null);
                        Assert.False(documents.Count == 0);
                        foreach (var (documentName, document) in documents) {
                            Assert.False(string.IsNullOrEmpty(documentName));
                            Assert.False(document.Url == null);
                            Assert.False(document.Url.Count == 0);
                            Assert.False(!document.Url.ContainsKey("Chinese"));
                            Assert.False(string.IsNullOrEmpty(document.Url["Chinese"]));
                        }
                    }

                    foreach (var (moduleType, modules) in mcu.Modules) {
                        Assert.False(string.IsNullOrEmpty(moduleType));
                        Assert.False(modules == null);
                        Assert.False(modules.Count == 0);
                        foreach (var (moduleName, module) in modules) {
                            Assert.False(string.IsNullOrEmpty(moduleName));
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