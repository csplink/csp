using System.Linq;
using CSP.Singleton.DB.Chip;
using CSP.Singleton.HAL.Config;
using CSP.Utils;
using Prism.Mvvm;

namespace CSP.Modules.Pages.MCU.ViewModels.Components.Package.LQFP;

public class LQFP144ViewModel : BindableBase
{
    public LQFP144ViewModel() {
        Pins = PinoutSingleton.Pinouts.Keys.ToArray();
        if (Pins.Length != 144) {
            MessageBoxUtil.Error($"读取引脚数据失败，LQFP144的引脚列表长度不为144，读取结果为{Pins.Length}");
        }
    }

    public string Company => SummarySingleton.Summary.Company;

    public string Name => SummarySingleton.Summary.Name;

    public string[] Pins { get; }
}