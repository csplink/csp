using System.IO;
using CSP.Models.DB;
using CSP.Models.HAL.Config;
using CSP.Resources;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Models.Tests.HAL.Config;

public class ClockModelTests
{
#if DEBUG
    private readonly string _mode = "Debug";
#else
    private readonly string _mode = "Release";
#endif
    private readonly ITestOutputHelper _testOutputHelper;

    public ClockModelTests(ITestOutputHelper testOutputHelper) {
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
                foreach (string version in package.Versions.Keys) {
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

                        string clockName = new DirectoryInfo(configDir).Name;
                        string clockPath = configDir + $"/clock/{clockName}.yml";

                        _testOutputHelper.WriteLine($"load file: {clockPath}");
                        ClockModel clock = ClockModel.Load(clockPath);
                        Assert.False(clock == null);
                        Assert.False(clock.Width <= 0);
                        Assert.False(clock.Height <= 0);
                        Assert.False(clock.Controls == null);
                        Assert.False(clock.Rects == null);
                        Assert.False(clock.Ellipses == null);

                        foreach (var (id, control) in clock.Controls) {
                            Assert.False(id <= 0);
                            Assert.False(control == null);
                            Assert.False(control.Base == null);
                            Assert.False(control.Base.Multiple < 0);
                            Assert.False(control.Base.DefaultValue < 0);
                            Assert.False(control.Base.DefaultIndex < 0);
                            Assert.False(string.IsNullOrWhiteSpace(control.Base.Name));
                            Assert.False(string.IsNullOrWhiteSpace(control.Base.Type));

                            if (control.Styles != null) {
                                foreach (var (styleName, style) in control.Styles) {
                                    Assert.False(string.IsNullOrWhiteSpace(styleName));
                                    Assert.False(style == null);
                                    Assert.False(style.Dependencies == null);
                                    Assert.False(style.Text == null);
                                    Assert.False(!style.Text.ContainsKey("zh-cn"));
                                    Assert.False(string.IsNullOrWhiteSpace(style.Status));
                                }
                            }
                        }

                        foreach (var (id, rect) in clock.Rects) {
                            Assert.False(id <= 0);
                            Assert.False(rect == null);
                            Assert.False(rect.X <= 0);
                            Assert.False(rect.Y <= 0);
                            Assert.False(rect.Width <= 0);
                            Assert.False(rect.Height <= 0);
                            Assert.False(!clock.Shapes.ContainsKey(id));
                        }

                        foreach (var (id, ellipse) in clock.Ellipses) {
                            Assert.False(id <= 0);
                            Assert.False(ellipse == null);
                            Assert.False(ellipse.X <= 0);
                            Assert.False(ellipse.Y <= 0);
                            Assert.False(ellipse.Width <= 0);
                            Assert.False(ellipse.Height <= 0);
                            Assert.False(!clock.Shapes.ContainsKey(id));
                        }
                    }
                }
            }
        }
    }
}