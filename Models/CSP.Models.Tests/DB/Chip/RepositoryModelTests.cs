using CSP.Models.DB.Chip;
using CSP.Resources;
using System.IO;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Models.Tests.DB.Chip
{
    public class RepositoryModelTests
    {
#if DEBUG
        private readonly string _mode = "Debug";
#else
        private readonly string _mode = "Release";
#endif
        private readonly ITestOutputHelper _testOutputHelper;

        public RepositoryModelTests(ITestOutputHelper testOutputHelper) {
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
            foreach (var (companyName, companies) in repository) {
                Assert.False(string.IsNullOrEmpty(companyName));
                Assert.False(companies == null);
                foreach (var (seriesName, series) in companies) {
                    Assert.False(string.IsNullOrEmpty(seriesName));
                    Assert.False(series == null);
                    foreach (var (lineName, lines) in series) {
                        Assert.False(string.IsNullOrEmpty(lineName));
                        Assert.False(lines == null);
                        foreach (var (mcuName, mcu) in lines) {
                            Assert.False(string.IsNullOrEmpty(mcuName));
                            Assert.False(mcu == null);

                            Assert.False(string.IsNullOrEmpty(mcu.Company));
                            Assert.False(string.IsNullOrEmpty(mcu.Series));
                            Assert.False(string.IsNullOrEmpty(mcu.Line));
                            Assert.False(string.IsNullOrEmpty(mcu.Name));
                            Assert.False(string.IsNullOrEmpty(mcu.Core));
                            Assert.False(string.IsNullOrEmpty(mcu.Package));

                            Assert.False(mcu.Current == null);
                            Assert.False(mcu.Peripherals == null);
                            Assert.False(mcu.Temperature == null);
                            Assert.False(mcu.Voltage == null);

                            Assert.False(mcu.Peripherals.Length == 0);

                            Assert.False(mcu.Flash <= 0);
                            Assert.False(mcu.Frequency <= 0);
                            Assert.False(mcu.IO <= 0);
                            Assert.False(mcu.Ram <= 0);

                            Assert.False(mcu.Current.Lowest <= 0);
                            Assert.False(mcu.Current.Run <= 0);
                            Assert.False(mcu.Temperature.Max <= 0);
                            Assert.False(mcu.Voltage.Max <= 0);

                            foreach (var peripheral in mcu.Peripherals) {
                                Assert.False(string.IsNullOrEmpty(peripheral.Type));
                                Assert.False(peripheral.Count <= 0);
                            }
                        }
                    }
                }
            }
        }
    }
}