using CSP.Modules.Pages.MCU.Models.Description;
using CSP.Modules.Pages.MCU.Tools;
using CSP.Utils;

namespace CSP.Modules.Pages.MCU.ViewModels.Components.Package.Espressif
{
    // ReSharper disable once InconsistentNaming
    public class ESP32_S3_WROOM_1ViewModel
    {
        public ESP32_S3_WROOM_1ViewModel() {
            if (Pins.Length != 40) {
                MessageBoxUtil.Error($"读取引脚数据失败，ESP32_S3_WROOM_1的引脚列表长度不为40，读取结果为{Pins.Length}");
            }
        }

        public string Company { get => DescriptionHelper.Company; }
        public string Name { get => DescriptionHelper.Name; }
        public PinoutModel.PinModel[] Pins { get => DescriptionHelper.Pinout.Pins; }
    }
}