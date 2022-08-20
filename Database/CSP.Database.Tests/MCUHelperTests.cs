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

            var solutionDir = File.ReadAllLines("./SolutionDir.txt")[0];
#if DEBUG
            IniFile.PathMCUDb = $"{solutionDir}/../csp_mcu_db";
            IniFile.PathRepository = $"{solutionDir}/..";
#else
            IniFile.PathMCUDb = $"{solutionDir}/Apps/CSP.Apps.Dev/bin/Release/net6.0-windows/Database/MCU";
            IniFile.PathRepository = $"{solutionDir}/.repository";
#endif
        }

        public void Dispose()
        {
            IniFile.Save();
        }

        [Fact]
        public void Test()
        {
            MCUHelper.LoadMcu("STMicroelectronics", "STM32F030C6Tx");

            Assert.False(MCUHelper.Repository == null);
            Assert.False(MCUHelper.GetMap("GPIO") == null);
            Assert.False(MCUHelper.MCU == null);
            Assert.False(MCUHelper.IP == null);
        }

        [Fact]
        public void GenerateMapTest()
        {
            MCUHelper.GenerateMap($"{IniFile.PathRepository}/csp_hal_apm32f1/drivers/csp_hal/inc/chal/gpio.h", @"./GPIO.xml");
        }
    }
}