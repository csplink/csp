using CSP.Database;
using CSP.Database.Models.MCU;
using CSP.Utils;
using Prism.Mvvm;
using Prism.Regions;

namespace CSP.Modules.Pages.MCU.ViewModels.Components.Package
{
    public class LQFP48ViewModel : BindableBase
    {
        public LQFP48ViewModel() {
            if (Pins.Length != 48) {
                MessageBoxUtil.Error($"读取引脚数据失败，LQFP48的引脚列表长度不为48，读取结果为{Pins.Length}");
            }
        }

        public string Company { get => MCUHelper.Company; }
        public string Name { get => MCUHelper.Name; }
        public MCUModel.PinModel[] Pins { get => MCUHelper.MCU.Pins; }
    }
}