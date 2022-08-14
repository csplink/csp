using CSP.Resources;
using System;
using System.IO;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Database.Tests
{
    public class MCUHelperTests : IDisposable
    {
        private readonly ITestOutputHelper _testOutputHelper;

        public MCUHelperTests(ITestOutputHelper testOutputHelper)
        {
            _testOutputHelper = testOutputHelper;
        }

        public void Dispose()
        {
            IniFile.Save();
        }

        [Fact]
        public void Test()
        {
            var solutionDir = File.ReadAllLines("./SolutionDir.txt")[0];
            IniFile.PathMCUDb = $"{solutionDir}.buildResources/Database/MCU";
            MCUHelper.LoadMcu("STMicroelectronics", "STM32F030C6Tx");

            Assert.False(MCUHelper.Repository == null);
            Assert.False(MCUHelper.GetMap("GPIO") == null);
            Assert.False(MCUHelper.MCU == null);
            Assert.False(MCUHelper.IP == null);
        }

        [Fact]
        public void GenerateMapTest()
        {
            var solutionDir = File.ReadAllLines("./SolutionDir.txt")[0];
            IniFile.PathMCUDb = $"{solutionDir}/../csp_mcu_db";
            IniFile.PathRepository = $"{solutionDir}/..";
            MCUHelper.GenerateMap($"{IniFile.PathRepository}/csp_hal_apm32f1/drivers/csp_hal/inc/chal/gpio.h", @"./GPIO.xml");
        }
    }
}