using System.Collections.Generic;
using System.IO;
using CSP.Models.DB;
using CSP.Models.HAL.Config;
using CSP.Resources;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Models.Tests.HAL.Config;

using ip_t = Dictionary<string, Dictionary<string, string[]>>;

public class IPModelTests
{
#if DEBUG
    private readonly string _mode = "Debug";
#else
    private readonly string _mode = "Release";
#endif
    private readonly ITestOutputHelper _testOutputHelper;

    public IPModelTests(ITestOutputHelper testOutputHelper) {
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
                _testOutputHelper.WriteLine($"load file: {Path.GetFullPath(file)}");
                PackageModel package = PackageModel.Load(file);
                Assert.False(package == null);
                foreach (string version in package.Versions.Keys) {
                    dir =
                        $"{solutionDir}/Apps/CSP.Apps.Dev/bin/{_mode}/net6.0-windows/csp_repo/repositories/{package.Category}/{package.Name}/{version}/config/map";
                    if (!Directory.Exists(dir)) {
                        continue;
                    }

                    string[] mapFiles = Directory.GetFiles(dir, "*.yml");
                    foreach (string mapFile in mapFiles) {
                        string fileName = Path.GetFileNameWithoutExtension(mapFile);

                        _testOutputHelper.WriteLine($"load file: {Path.GetFullPath(mapFile)}");
                        MapModel map = MapModel.Load(mapFile);
                        Assert.False(map == null);
                        string[] configDirs = Directory.GetDirectories($"{dir}/../");
                        foreach (string configDir in configDirs) {
                            string pinoutPath = $"{configDir}/pinout.yml";
                            if (!File.Exists(pinoutPath)) {
                                continue;
                            }

                            string ipFile = $"{configDir}/ip/{fileName}.yml";

                            _testOutputHelper.WriteLine($"load file: {Path.GetFullPath(ipFile)}");
                            ip_t ip = IPModel.Load(ipFile).Content;
                            Assert.False(ip == null);
                            foreach (var (ipName, ipValue) in ip) {
                                Assert.False(string.IsNullOrWhiteSpace(ipName));
                                Assert.False(ipValue == null);
                                Assert.False(ipValue.Count == 0);
                                Assert.False(map.Groups.ContainsKey(ipName));
                                foreach (var (key, value) in ipValue) {
                                    Assert.False(string.IsNullOrWhiteSpace(key));
                                    Assert.False(value == null);
                                    Assert.False(value.Length == 0);
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}