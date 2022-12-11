﻿using CSP.Utils;
using Prism.Mvvm;

namespace CSP.Modules.Pages.MCU.ViewModels.Components.Package.LQFP;

public class LQFP48ViewModel : BindableBase
{
    public LQFP48ViewModel() {
        if (Pins.Length != 48) {
            MessageBoxUtil.Error($"读取引脚数据失败，LQFP48的引脚列表长度不为48，读取结果为{Pins.Length}");
        }
    }

    public string Company => DescriptionHelper.Company;

    public string Name => DescriptionHelper.Name;

    public PinoutModel.PinModel[] Pins => DescriptionHelper.Pinout.Pins;
}