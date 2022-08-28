using CSP.Modules.Dialogs.NewMCU.Models;
using CSP.Resources;
using System.IO;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Modules.Dialogs.NewMCU.Tests.Models
{
    public class MCUAndRepositoryModelTests
    {
        private readonly ITestOutputHelper _testOutputHelper;

        public MCUAndRepositoryModelTests(ITestOutputHelper testOutputHelper) {
            _testOutputHelper = testOutputHelper;

            var solutionDir = File.ReadAllLines("./SolutionDir.txt")[0];
#if DEBUG
            IniFile.PathMCUDb = $"{solutionDir}/../csp_mcu_db";
            IniFile.PathRepository = $"{solutionDir}/..";
#else
            IniFile.PathMCUDb = $"{solutionDir}/Apps/CSP.Apps.Dev/bin/Release/net6.0-windows/Database/MCU";
            IniFile.PathRepository = $"{solutionDir}/.repository";
#endif
        }

        public void Dispose() {
            IniFile.Save();
        }

        [Fact]
        public void LoadTest() {
            var repository = RepositoryModel.Load($"{IniFile.PathMCUDb}/Repository.xml");
            foreach (var company in repository.Companies) {
                foreach (var series in company.Series) {
                    foreach (var line in series.Lines) {
                        foreach (var mcu in line.MCU) {
                            Assert.False(mcu == null);
                            Assert.False(mcu.Company == null);
                            Assert.False(mcu.Core == null);

                            Assert.False(mcu.Current == null);
                            Assert.False(mcu.Current.Lowest == 0);
                            Assert.False(mcu.Current.Run == 0);

                            Assert.False(mcu.Flash == 0);
                            Assert.False(mcu.Frequency == 0);
                            Assert.False(mcu.IO == 0);

                            Assert.False(mcu.Line == null);
                            Assert.False(mcu.Name == null);

                            Assert.False(mcu.Peripherals == null);
                            foreach (var peripherals in mcu.Peripherals) {
                                Assert.False(peripherals.Number == 0);
                                Assert.False(peripherals.Type == null);
                            }

                            //  Assert.False(mcu.Price == null);
                            Assert.False(mcu.Ram == 0);
                            Assert.False(mcu.Series == null);

                            Assert.False(mcu.Temperature == null);
                            Assert.False(mcu.Temperature.Max == 0);
                            Assert.False(mcu.Temperature.Min == 0);

                            Assert.False(mcu.Voltage == null);
                            Assert.False(mcu.Voltage.Max == 0);
                            Assert.False(mcu.Voltage.Min == 0);

                            var m = MCUModel.Load($"{IniFile.PathMCUDb}/{mcu.Company}/{mcu.Name}.xml");
                            Assert.False(m.ClockTree == null);
                            Assert.False(m.Company == null);
                            Assert.False(m.CompanyUrl == null);

                            Assert.False(m.HAL == null);
                            Assert.False(m.HAL.Name == null);
                            Assert.False(m.HAL.Version == null);

                            Assert.False(m.Illustrate == null);
                            Assert.False(m.Introduction == null);
                            Assert.False(m.IoType == null);
                            Assert.False(m.Line == null);
                            Assert.False(m.Modules == null);
                            foreach (var modules in m.Modules) {
                                Assert.False(modules.Name == null);
                                Assert.False(modules.Categories == null);
                                foreach (var category in modules.Categories) {
                                    Assert.False(category.Name == null);
                                }
                            }

                            Assert.False(m.Name == null);
                            Assert.False(m.Package == null);
                            // Assert.False(m.Price == 0);
                            Assert.False(m.RepositoryUrl == null);
                            Assert.False(m.Series == null);
                            Assert.False(m.Url == null);
                        }
                    }
                }
            }
        }
    }
}