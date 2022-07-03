using System;
using System.IO;
using CSP.Database.Models.MCU;
using CSP.Utils.Extensions;

namespace CSP.Modules.Pages.MCU.Services.Generate
{
    public class GenerateService
    {
        public static void Generate(MCUModel mcu, string path)
        {
            if (mcu == null)
                throw new ArgumentNullException("mcu null");

            var pathInc = $"{path}/misfra_studio/inc";
            var pathSrc = $"{path}/misfra_studio/src";

            if (!Directory.Exists(pathInc))
                Directory.CreateDirectory(pathInc);
            if (!Directory.Exists(pathSrc))
                Directory.CreateDirectory(pathSrc);

            foreach (var module in mcu.Modules)
            {
                foreach (var category in module.Categories)
                {
                    switch (category.Name.ToUpper())
                    {
                        case "GPIO":
                            {
                                GenerateGPIO(mcu, path);
                            }
                            break;
                    }
                }
            }
        }

        public static void GenerateGPIO(MCUModel mcu, string path)
        {
            if (mcu == null)
                throw new ArgumentNullException("mcu null");

            var pathInc = $"{path}/misfra_studio/inc/ms_gpio.h";
            var pathSrc = $"{path}/misfra_studio/src/ms_gpio.c";

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