// Licensed under the Apache License, Version 2.0 (the "License");
// You may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// Copyright (C) 2022-2023 xqyjlj<xqyjlj@126.com>
//
// @author      xqyjlj
// @file        LFBGA337ViewModel.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System.Linq;
using CSP.Singleton.DB.Chip;
using CSP.Singleton.HAL.Config;
using Prism.Mvvm;

namespace CSP.Modules.Pages.MCU.ViewModels.Components.Package.LFBGA;

public class LFBGA337ViewModel : BindableBase
{
    public LFBGA337ViewModel() {
        Pins = PinoutSingleton.Pinouts.Keys.ToArray();
        // if (Pins.Length != 144) {
        //     MessageBoxUtil.Error($"读取引脚数据失败，LQFP144的引脚列表长度不为144，读取结果为{Pins.Length}");
        // }
    }

    public string Company => SummarySingleton.Summary.Company;

    public string Name => SummarySingleton.Summary.Name;

    public string[] Pins { get; }
}