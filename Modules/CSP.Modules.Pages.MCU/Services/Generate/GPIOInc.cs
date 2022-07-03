using CSP.Database.Models.MCU;
using CSP.Modules.Pages.MCU.Services.Generate.Models;
using CSP.Utils.Extensions;

namespace CSP.Modules.Pages.MCU.Services.Generate
{
    public class GPIOInc : IncBase
    {
        public GPIOInc(MCUModel mcu = null, string path = null) : base(path)
        {
            File = "ms_gpio.h";
            Brief = "This file provides code for the configuration of all used GPIO.";

            AddInclude(new IncModel()
            {
                IsSys = false,
                Name = "misfra_driver/gpio.h"
            });

            var functionDeclaration = new FunctionDeclarationModel
            {
                Name = "ms_gpio_init",
                Type = "void"
            };
            functionDeclaration.Parameters.Add(new FunctionDeclarationModel.ParameterModel()
            {
                Name = "",
                Type = "void"
            });
            AddFunctionDeclaration(functionDeclaration);

            if (mcu == null)
                return;

            foreach (var pin in mcu.Pins)
            {
                if (((MCUModel.PinModel.DataContextModel)pin.GPIOProperty.Data).IsLocked)
                {
                    var ext = new ExternModel()
                    {
                        Name = ((MCUModel.PinModel.DataContextModel)pin.GPIOProperty.Data).Name,
                        Type = "md_gpio_obj_t"
                    };
                    AddExtern(ext);

                    if (!((MCUModel.PinModel.DataContextModel)pin.GPIOProperty.Data).Label.IsNullOrEmpty())
                    {
                        var macro = new MacroModel()
                        {
                            Name = ((MCUModel.PinModel.DataContextModel)pin.GPIOProperty.Data).Label,
                            Value = ((MCUModel.PinModel.DataContextModel)pin.GPIOProperty.Data).Name
                        };
                        AddMacro(macro);
                    }
                }
            }
        }
    }
}