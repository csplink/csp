using CSP.Modules.Pages.MCU.Models;
using CSP.Modules.Pages.MCU.Services.Generate.Models;
using CSP.Utils.Extensions;

namespace CSP.Modules.Pages.MCU.Services.Generate
{
    public class GPIOInc : IncBase
    {
        public GPIOInc(PinoutModel mcu = null, string path = null) : base(path) {
            File = "gpio.h";
            Brief = "This file provides code for the configuration of all used GPIO.";

            AddInclude(new IncModel() {
                IsSys = false,
                Name = "chal/gpio.h"
            });

            var functionDeclaration = new FunctionDeclarationModel {
                Name = "csp_gpio_init",
                Type = "void"
            };
            functionDeclaration.Parameters.Add(new FunctionDeclarationModel.ParameterModel() {
                Name = "",
                Type = "void"
            });
            AddFunctionDeclaration(functionDeclaration);

            if (mcu == null)
                return;

            // foreach (var pin in mcu.Pins) {
            //     if (pin.BaseProperty.IsLocked) {
            //         if (!pin.BaseProperty.Label.IsNullOrEmpty()) {
            //             var macro = new MacroModel {
            //                 Name = pin.BaseProperty.Label,
            //                 Value = pin.BaseProperty.Name
            //             };
            //             AddMacro(macro);
            //         }
            //     }
            // }
        }
    }
}