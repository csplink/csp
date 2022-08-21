using CSP.Modules.Pages.MCU.Services.Generate;
using System.IO;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Modules.Pages.MCU.Tests.Services.Generate
{
    public class GPIOIncTests
    {
        private readonly ITestOutputHelper _testOutputHelper;

        public GPIOIncTests(ITestOutputHelper testOutputHelper)
        {
            _testOutputHelper = testOutputHelper;
        }

        [Fact]
        public void Test()
        {
            var gpioInc = new GPIOInc();
            var inc = gpioInc.Generate();

            const string path = "./csp/inc";

            if (!Directory.Exists(path))
                Directory.CreateDirectory(path);

            var sw = new StreamWriter($"{path}/csp_gpio.h", false);
            sw.Write(inc);
            sw.Close();
        }
    }
}