using CSP.Modules.Pages.MCU.Models.Repository;
using CSP.Modules.Pages.MCU.Services.Generate.Models;

namespace CSP.Modules.Pages.MCU.Services.Generate
{
    public class GPIOSrc : SrcBase
    {
        public GPIOSrc(PinoutModel mcu = null, string path = null) : base(path) {
            File = "csp_gpio.c";
            Brief = "This file provides code for the configuration of all used GPIO.";

            AddInclude(new IncModel() {
                IsSys = false,
                Name = "csp/gpio.h"
            });

            if (mcu == null)
                return;

            var function = new FunctionModel {
                Name = "csp_gpio_init",
                Type = "int"
            };
            function.Parameters.Add(new FunctionModel.ParameterModel() {
                Name = "",
                Type = "void"
            });

            // foreach (var pin in mcu.Pins)
            // {
            //     if (((PinOutModel.PinModel.DataContextModel)pin.GPIOProperty.Data).IsLocked)
            //     {
            //         switch (((PinOutModel.PinModel.DataContextModel)pin.GPIOProperty.Data).Function)
            //         {
            //             case "GPIO-Input":
            //                 {
            //                     var functionUse = new FunctionModel.FunctionUseModel
            //                     {
            //                         Name = "chal_gpio_init"
            //                     };
            //                     functionUse.Parameters.Add(pin.Name);
            //                     functionUse.Parameters.Add(((PinOutModel.PinModel.DataContextModel)pin.GPIOProperty.Data).Mode.String);
            //                     functionUse.Parameters.Add("-1");
            //                     functionUse.Parameters.Add(((PinOutModel.PinModel.DataContextModel)pin.GPIOProperty.Data).Pull.String);
            //                     function.FunctionUses.Add(functionUse);
            //                 }
            //                 break;
            //
            //             case "GPIO-Output":
            //                 {
            //                     var functionUse = new FunctionModel.FunctionUseModel
            //                     {
            //                         Name = "chal_gpio_write_pin"
            //                     };
            //                     functionUse.Parameters.Add(pin.Name);
            //                     functionUse.Parameters.Add(((PinOutModel.PinModel.DataContextModel)pin.GPIOProperty.Data).Level.String);
            //                     function.FunctionUses.Add(functionUse);
            //
            //                     functionUse = new FunctionModel.FunctionUseModel
            //                     {
            //                         Name = "chal_gpio_init"
            //                     };
            //                     functionUse.Parameters.Add(pin.Name);
            //                     functionUse.Parameters.Add(((PinOutModel.PinModel.DataContextModel)pin.GPIOProperty.Data).Mode.String);
            //                     functionUse.Parameters.Add(((PinOutModel.PinModel.DataContextModel)pin.GPIOProperty.Data).Speed.String);
            //                     functionUse.Parameters.Add(((PinOutModel.PinModel.DataContextModel)pin.GPIOProperty.Data).Pull.String);
            //                     function.FunctionUses.Add(functionUse);
            //                 }
            //                 break;
            //
            //             case "GPIO-Analog":
            //                 {
            //                     var functionUse = new FunctionModel.FunctionUseModel
            //                     {
            //                         Name = "chal_gpio_init"
            //                     };
            //                     functionUse.Parameters.Add(pin.Name);
            //                     functionUse.Parameters.Add(((PinOutModel.PinModel.DataContextModel)pin.GPIOProperty.Data).Mode.String);
            //                     functionUse.Parameters.Add("-1");
            //                     functionUse.Parameters.Add(((PinOutModel.PinModel.DataContextModel)pin.GPIOProperty.Data).Pull.String);
            //                     function.FunctionUses.Add(functionUse);
            //                 }
            //                 break;
            //
            //             case "GPIO-EXTI":
            //                 {
            //                 }
            //                 break;
            //         }
            //     }
            // }

            AddFunction(function);

            AddInit("csp_gpio_init");
        }
    }
}