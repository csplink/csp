using CSP.Utils;
using Prism.Mvvm;

namespace CSP.Modules.Pages.MCU.ViewModels.Components.Package.LQFP;

public class LQFP144ViewModel : BindableBase
{
    public LQFP144ViewModel() {
        if (Pins.Length != 144) {
            MessageBoxUtil.Error($"读取引脚数据失败，LQFP144的引脚列表长度不为144，读取结果为{Pins.Length}");
        }
    }

    public string Company => DescriptionHelper.Company;

    public string Name => DescriptionHelper.Name;

    public PinoutModel.PinModel[] Pins => DescriptionHelper.Pinout.Pins;
}