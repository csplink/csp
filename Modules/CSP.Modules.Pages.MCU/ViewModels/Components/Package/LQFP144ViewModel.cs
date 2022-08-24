using CSP.Database;
using CSP.Database.Models.MCU;
using CSP.Utils;
using Prism.Mvvm;
using Prism.Regions;

namespace CSP.Modules.Pages.MCU.ViewModels.Components.Package
{
    public class LQFP144ViewModel : BindableBase
    {
        public LQFP144ViewModel() {
            if (Pins.Length != 144) {
                MessageBoxUtil.Error($"读取引脚数据失败，LQFP144的引脚列表长度不为144，读取结果为{Pins.Length}");
            }
        }

        public string Company { get => MCUHelper.Company; }
        public string Name { get => MCUHelper.Name; }
        public MCUModel.PinModel[] Pins { get => MCUHelper.MCU.Pins; }
    }
}