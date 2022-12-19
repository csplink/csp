using System.Linq;
using CSP.Singleton.DB.Chip;
using CSP.Singleton.HAL.Config;
using CSP.Utils;
using Prism.Mvvm;

namespace CSP.Modules.Pages.MCU.ViewModels.Components.Package.LQFP;

public class LQFP64ViewModel : BindableBase
{
    public LQFP64ViewModel() {
        Pins = PinoutSingleton.Pinouts.Keys.ToArray();
        if (Pins.Length != 64) {
            MessageBoxUtil.Error($"读取引脚数据失败，LQFP64的引脚列表长度不为64，读取结果为{Pins.Length}");
        }
    }

    public string Company => SummarySingleton.Summary.Company;

    public string Name => SummarySingleton.Summary.Name;

    public string[] Pins { get; }
}