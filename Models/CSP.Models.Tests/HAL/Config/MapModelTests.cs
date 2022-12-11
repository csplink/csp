using System.IO;
using CSP.Models.DB;
using CSP.Models.HAL.Config;
using CSP.Resources;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Models.Tests.HAL.Config;

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
        ConfigFile.Save();
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
                foreach (string version in package.Versions) {
                    dir =
                        $"{solutionDir}/Apps/CSP.Apps.Dev/bin/{_mode}/net6.0-windows/csp_repo/repositories/{package.Category}/{package.Name}/{version}/config/map";
                    if (!Directory.Exists(dir)) {
                        continue;
                    }

                    string[] mapFiles = Directory.GetFiles(dir, "*.yml");
                    foreach (string mapFile in mapFiles) {
                        _testOutputHelper.WriteLine($"load file: {mapFile}");
                        MapModel map = MapModel.Load(mapFile);
                        Assert.False(map == null);
                        Assert.False(map.Groups == null);
                        Assert.False(map.Properties == null);

                        Assert.False(map.Groups.Count == 0);
                        Assert.False(map.Properties.Count == 0);

                        foreach (var (groupName, group) in map.Groups) {
                            Assert.False(group == null);
                            Assert.False(string.IsNullOrWhiteSpace(groupName));
                            Assert.False(!group.Comment.ContainsKey("zh-cn"));
                            Assert.False(group.Values == null);
                            Assert.False(group.Values.Count == 0);

                            foreach (var (valueName, value) in group.Values) {
                                Assert.False(value == null);
                                Assert.False(string.IsNullOrWhiteSpace(valueName));
                                Assert.False(!value.Comment.ContainsKey("zh-cn"));
                            }
                        }

                        foreach (var (propertyName, property) in map.Properties) {
                            Assert.False(property == null);
                            Assert.False(string.IsNullOrWhiteSpace(propertyName));
                            Assert.False(!property.DisplayName.ContainsKey("zh-cn"));
                            Assert.False(!property.Description.ContainsKey("zh-cn"));
                            Assert.False(string.IsNullOrWhiteSpace(property.Category));
                        }
                    }
                }
            }
        }
    }
}