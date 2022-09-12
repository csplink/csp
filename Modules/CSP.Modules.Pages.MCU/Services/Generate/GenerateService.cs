using CSP.Modules.Pages.MCU.Models.Repository;
using System;
using System.IO;

namespace CSP.Modules.Pages.MCU.Services.Generate
{
    public class GenerateService
    {
        public static void Generate(PinoutModel mcu, string path) {
            if (mcu == null)
                throw new ArgumentNullException(nameof(mcu));

            var pathInc = $"{path}/csp/inc/csp";
            var pathSrc = $"{path}/csp/src";

            if (!Directory.Exists(pathInc))
                Directory.CreateDirectory(pathInc);
            if (!Directory.Exists(pathSrc))
                Directory.CreateDirectory(pathSrc);

            // foreach (var module in mcu.Modules) {
            //     foreach (var category in module.Categories) {
            //         switch (category.Name.ToUpper()) {
            //             case "GPIO": {
            //                     GenerateGPIO(mcu, path);
            //                 }
            //                 break;
            //         }
            //     }
            // }
        }

        public static void GenerateGPIO(PinoutModel mcu, string path) {
            if (mcu == null)
                throw new ArgumentNullException(nameof(mcu));

            var pathInc = $"{path}/csp/inc/csp/gpio.h";
            var pathSrc = $"{path}/csp/src/csp_gpio.c";

            var gpioInc = new GPIOInc(mcu);
            var inc = gpioInc.Generate();

            var sw = new StreamWriter($"{pathInc}", false);
            sw.Write(inc);
            sw.Close();

            var gpioSrc = new GPIOSrc(mcu);
            var src = gpioSrc.Generate();

            sw = new StreamWriter($"{pathSrc}", false);
            sw.Write(src);
            sw.Close();
        }
    }
}