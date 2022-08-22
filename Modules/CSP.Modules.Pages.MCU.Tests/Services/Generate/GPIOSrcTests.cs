using CSP.Modules.Pages.MCU.Services.Generate;
using CSP.Modules.Pages.MCU.Services.Generate.Models;
using System.IO;
using Xunit;
using Xunit.Abstractions;

// ReSharper disable StringLiteralTypo

namespace CSP.Modules.Pages.MCU.Tests.Services.Generate
{
    public class GPIOSrcTests
    {
        private readonly ITestOutputHelper _testOutputHelper;

        public GPIOSrcTests(ITestOutputHelper testOutputHelper) {
            _testOutputHelper = testOutputHelper;
        }

        [Fact]
        public void Test() {
            var gpioSrc = new GPIOSrc();

            var ext = new ExternModel() {
                Name = "PA0",
                Type = "md_gpio_obj_t"
            };
            gpioSrc.AddExtern(ext);

            ext = new ExternModel() {
                Name = "PA1",
                Type = "md_gpio_obj_t"
            };
            gpioSrc.AddExtern(ext);

            var variable = new VariableModel() {
                Name = "PA0",
                IsStatic = false,
                Type = "md_gpio_obj_t",
                Value = "{GPIOA, GPIO_PIN_0, EXTI0_1_IRQn}"
            };
            gpioSrc.AddVariable(variable);

            variable = new VariableModel() {
                Name = "PA1",
                IsStatic = false,
                Type = "md_gpio_obj_t",
                Value = "{GPIOA, GPIO_PIN_1, EXTI0_1_IRQn}"
            };
            gpioSrc.AddVariable(variable);

            var function = new FunctionModel {
                Name = "ms_gpio_init",
                Type = "void"
            };
            function.Parameters.Add(new FunctionModel.ParameterModel() {
                Name = "",
                Type = "void"
            });

            var functionUse = new FunctionModel.FunctionUseModel {
                Name = "md_gpio_set_mode"
            };
            functionUse.Parameters.Add("&PA0");
            functionUse.Parameters.Add("MD_GPIO_MODE_OUTPUT_PP");
            functionUse.Parameters.Add("MD_GPIO_SPEED_LOW");
            functionUse.Parameters.Add("MD_GPIO_PULL_DOWN");
            function.FunctionUses.Add(functionUse);

            functionUse = new FunctionModel.FunctionUseModel {
                Name = "md_gpio_set_mode"
            };

            functionUse.Parameters.Add("&PA1");
            functionUse.Parameters.Add("MD_GPIO_MODE_OUTPUT_PP");
            functionUse.Parameters.Add("MD_GPIO_SPEED_LOW");
            functionUse.Parameters.Add("MD_GPIO_PULL_DOWN");
            function.FunctionUses.Add(functionUse);

            gpioSrc.AddFunction(function);

            var src = gpioSrc.Generate();

            const string path = "./csp/src";

            if (!Directory.Exists(path))
                Directory.CreateDirectory(path);

            var sw = new StreamWriter($"{path}/csp_gpio.c", false);
            sw.Write(src);
            sw.Close();
        }
    }
}