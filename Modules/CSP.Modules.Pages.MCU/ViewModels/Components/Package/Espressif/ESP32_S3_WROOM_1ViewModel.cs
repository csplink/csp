using System.Linq;
using CSP.Singleton.DB.Chip;
using CSP.Singleton.HAL.Config;
using CSP.Utils;

namespace CSP.Modules.Pages.MCU.ViewModels.Components.Package.Espressif;

// ReSharper disable once InconsistentNaming
public class ESP32_S3_WROOM_1ViewModel
{
    public ESP32_S3_WROOM_1ViewModel() {
        Pins = PinoutSingleton.Pinouts.Keys.ToArray();
        if (Pins.Length != 40) {
            MessageBoxUtil.Error($"读取引脚数据失败，ESP32_S3_WROOM_1的引脚列表长度不为40，读取结果为{Pins.Length}");
        }
    }

    public string Company => SummarySingleton.Summary.Company;

    public string Name => SummarySingleton.Summary.Name;

    public string[] Pins { get; }
}