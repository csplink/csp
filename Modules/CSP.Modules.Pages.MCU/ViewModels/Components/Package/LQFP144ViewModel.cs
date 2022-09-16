using CSP.Modules.Pages.MCU.Models.Description;
using CSP.Modules.Pages.MCU.Tools;
using CSP.Utils;
using Prism.Mvvm;

namespace CSP.Modules.Pages.MCU.ViewModels.Components.Package
{
    public class LQFP144ViewModel : BindableBase
    {
        public LQFP144ViewModel() {
            if (Pins.Length != 144) {
                MessageBoxUtil.Error($"读取引脚数据失败，LQFP144的引脚列表长度不为144，读取结果为{Pins.Length}");
            }
        }

        public string Company { get => DescriptionHelper.Company; }
        public string Name { get => DescriptionHelper.Name; }
        public PinoutModel.PinModel[] Pins { get => DescriptionHelper.Pinout.Pins; }
    }
}