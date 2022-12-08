﻿using CSP.Models.DB.Chip;
using CSP.Resources;
using System.IO;
using Xunit;
using Xunit.Abstractions;
using Xunit.Sdk;

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
            _testOutputHelper.WriteLine($"load file: {path}");
            var repository = RepositoryModel.Load(path);
            foreach (var (companyName, companies) in repository) {
                Assert.False(string.IsNullOrWhiteSpace(companyName));
                Assert.False(companies == null);
                foreach (var (seriesName, series) in companies) {
                    Assert.False(string.IsNullOrWhiteSpace(seriesName));
                    Assert.False(series == null);
                    foreach (var (lineName, lines) in series) {
                        Assert.False(string.IsNullOrWhiteSpace(lineName));
                        Assert.False(lines == null);
                        foreach (var (mcuName, mcu) in lines) {
                            Assert.False(string.IsNullOrWhiteSpace(mcuName));
                            Assert.False(mcu == null);

                            Assert.False(string.IsNullOrWhiteSpace(mcu.Company));
                            Assert.False(string.IsNullOrWhiteSpace(mcu.Series));
                            Assert.False(string.IsNullOrWhiteSpace(mcu.Line));
                            Assert.False(string.IsNullOrWhiteSpace(mcu.Name));
                            Assert.False(string.IsNullOrWhiteSpace(mcu.Core));
                            Assert.False(string.IsNullOrWhiteSpace(mcu.Package));

                            Assert.False(mcu.Current == null);
                            Assert.False(mcu.Peripherals == null);
                            Assert.False(mcu.Temperature == null);
                            Assert.False(mcu.Voltage == null);

                            Assert.False(mcu.Peripherals.Count == 0);

                            Assert.False(mcu.Flash <= 0);
                            Assert.False(mcu.Frequency <= 0);
                            Assert.False(mcu.IO <= 0);
                            Assert.False(mcu.Ram <= 0);

                            Assert.False(mcu.Current.Lowest <= 0);
                            Assert.False(mcu.Current.Run <= 0);
                            Assert.False(mcu.Temperature.Max <= 0);
                            Assert.False(mcu.Voltage.Max <= 0);

                            foreach (var (peripheralName, peripheralCount) in mcu.Peripherals) {
                                Assert.False(string.IsNullOrWhiteSpace(peripheralName));
                                Assert.False(peripheralCount <= 0);
                            }
                        }
                    }
                }
            }
        }
    }
}