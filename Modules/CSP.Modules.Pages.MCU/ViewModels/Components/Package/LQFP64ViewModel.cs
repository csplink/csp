using CSP.Modules.Pages.MCU.Models.Description;
using CSP.Modules.Pages.MCU.Tools;
using CSP.Utils;
using Prism.Mvvm;

namespace CSP.Modules.Pages.MCU.ViewModels.Components.Package
{
    public class LQFP64ViewModel : BindableBase
    {
        public LQFP64ViewModel() {
            if (Pins.Length != 64) {
                MessageBoxUtil.Error($"读取引脚数据失败，LQFP64的引脚列表长度不为64，读取结果为{Pins.Length}");
            }
        }

        public string Company { get => DescriptionHelper.Company; }
        public string Name { get => DescriptionHelper.Name; }
        public PinoutModel.PinModel[] Pins { get => DescriptionHelper.Pinout.Pins; }
    }
}