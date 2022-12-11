using System.Collections.Generic;
using System.IO;
using CSP.Models.DB;
using CSP.Models.HAL.Config;
using CSP.Resources;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Models.Tests.HAL.Config;

public class PinoutModelTests
{
#if DEBUG
    private readonly string _mode = "Debug";
#else
    private readonly string _mode = "Release";
#endif
    private readonly ITestOutputHelper _testOutputHelper;

    public PinoutModelTests(ITestOutputHelper testOutputHelper) {
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
                        $"{solutionDir}/Apps/CSP.Apps.Dev/bin/{_mode}/net6.0-windows/csp_repo/repositories/{package.Category}/{package.Name}/{version}/config";
                    if (!Directory.Exists(dir)) {
                        continue;
                    }

                    string[] configDirs = Directory.GetDirectories(dir);
                    foreach (string configDir in configDirs) {
                        string pinoutPath = $"{configDir}/pinout.yml";
                        if (!File.Exists(pinoutPath)) {
                            continue;
                        }

                        _testOutputHelper.WriteLine($"load file: {pinoutPath}");
                        Dictionary<string, PinoutModel> pinouts = PinoutModel.Load(pinoutPath);
                        Assert.False(pinouts == null);
                        int position = 0; // must be sorted by position
                        foreach (var (pinName, pinout) in pinouts) {
                            Assert.False(pinout == null);
                            Assert.False(string.IsNullOrWhiteSpace(pinName));
                            Assert.False(string.IsNullOrWhiteSpace(pinout.Type));
                            Assert.False(position >= pinout.Position);

                            position = pinout.Position;
                        }
                    }
                }
            }
        }
    }
}