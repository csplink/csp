using System.Linq;
using CSP.Singleton.DB.Chip;
using CSP.Singleton.HAL.Config;
using CSP.Utils;
using Prism.Mvvm;

namespace CSP.Modules.Pages.MCU.ViewModels.Components.Package.LQFP;

public class LQFP48ViewModel : BindableBase
{
    public LQFP48ViewModel() {
        Pins = PinoutSingleton.Pinouts.Keys.ToArray();
        if (Pins.Length != 48) {
            MessageBoxUtil.Error($"读取引脚数据失败，LQFP48的引脚列表长度不为48，读取结果为{Pins.Length}");
        }
    }

    public string Company => SummarySingleton.Summary.Company;

    public string Name => SummarySingleton.Summary.Name;

    public string[] Pins { get; }
}