using CSP.Database;
using CSP.Database.Models.MCU;
using CSP.Utils;
using Prism.Mvvm;
using Prism.Regions;

namespace CSP.Modules.Pages.MCU.ViewModels.Components.Package
{
    public class LQFP64ViewModel : BindableBase
    {
        public LQFP64ViewModel() {
            if (Pins.Length != 64) {
                MessageBoxUtil.Error($"读取引脚数据失败，LQFP64的引脚列表长度不为64，读取结果为{Pins.Length}");
            }
        }

        public string Company { get => MCUHelper.Company; }
        public string Name { get => MCUHelper.Name; }
        public MCUModel.PinModel[] Pins { get => MCUHelper.MCU.Pins; }
    }
}