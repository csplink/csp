using CSP.Models.DB;
using CSP.Models.HAL.Config;
using CSP.Resources;
using System;
using System.IO;
using System.Windows.Shapes;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Models.Tests.HAL.Config
{
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
                    _testOutputHelper.WriteLine($"load file: {file}");
                    var package = PackageModel.Load(file);
                    foreach (var version in package.Versions) {
                        dir = $"{solutionDir}/Apps/CSP.Apps.Dev/bin/{_mode}/net6.0-windows/csp_repo/repositories/{package.Category}/{package.Name}/{version}/config";
                        if (!Directory.Exists(dir))
                            continue;
                        var configDirs = Directory.GetDirectories(dir);
                        foreach (var configDir in configDirs) {
                            var pinoutPath = $"{configDir}/pinout.yml";
                            if (!File.Exists(pinoutPath))
                                continue;
                            _testOutputHelper.WriteLine($"load file: {pinoutPath}");
                            var pinouts = PinoutModel.Load(pinoutPath);
                            Assert.False(pinouts == null);
                            var position = 0; // must be sorted by position
                            foreach (var (pinName, pinout) in pinouts) {
                                Assert.False(pinout == null);
                                Assert.False(string.IsNullOrEmpty(pinName));
                                Assert.False(string.IsNullOrEmpty(pinout.Type));
                                Assert.False(position >= pinout.Position);

                                position = pinout.Position;
                            }
                        }
                    }
                }
            }
        }
    }
}