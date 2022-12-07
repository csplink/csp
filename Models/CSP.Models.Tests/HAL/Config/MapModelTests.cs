using CSP.Models.DB;
using CSP.Models.HAL.Config;
using CSP.Resources;
using System.IO;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Models.Tests.HAL.Config
{
    public class MapModelTests
    {
#if DEBUG
        private readonly string _mode = "Debug";
#else
        private readonly string _mode = "Release";
#endif
        private readonly ITestOutputHelper _testOutputHelper;

        public MapModelTests(ITestOutputHelper testOutputHelper) {
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
                    foreach (var version in package.Versions) {
                        dir = $"{solutionDir}/Apps/CSP.Apps.Dev/bin/{_mode}/net6.0-windows/csp_repo/repositories/{package.Category}/{package.Name}/{version}/config/map";
                        if (!Directory.Exists(dir))
                            continue;
                        var mapFiles = Directory.GetFiles(dir, "*.yml");
                        foreach (var mapFile in mapFiles) {
                            var map = MapModel.Load(mapFile);
                            Assert.False(map == null);
                            Assert.False(map.Groups == null);
                            Assert.False(map.Properties == null);

                            Assert.False(map.Groups.Count == 0);
                            Assert.False(map.Properties.Count == 0);

                            foreach (var (groupName, group) in map.Groups) {
                                Assert.False(group == null);
                                Assert.False(string.IsNullOrEmpty(groupName));
                                Assert.False(!group.Comment.ContainsKey("Chinese"));
                                Assert.False(group.Values == null);
                                Assert.False(group.Values.Count == 0);

                                foreach (var (valueName, value) in group.Values) {
                                    Assert.False(value == null);
                                    Assert.False(string.IsNullOrEmpty(valueName));
                                    Assert.False(!value.Comment.ContainsKey("Chinese"));
                                }
                            }

                            foreach (var (propertyName, property) in map.Properties) {
                                Assert.False(property == null);
                                Assert.False(string.IsNullOrEmpty(propertyName));
                                Assert.False(!property.DisplayName.ContainsKey("Chinese"));
                                Assert.False(!property.Description.ContainsKey("Chinese"));
                                Assert.False(string.IsNullOrEmpty(property.Category));
                            }
                        }
                    }
                }
            }
        }
    }
}