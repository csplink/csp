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
// @file        PinConfigSingleton.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System;
using System.Collections.Generic;
using CSP.Models.HAL.Config;
using CSP.Models.Internal;
using CSP.Utils;

namespace CSP.Singleton.Internal;

public static class PinConfigSingleton
{
    private static readonly PinConfigSingletonInstance Instance = PinConfigSingletonInstance.Instance;

    public static Dictionary<string, PinConfigModel> PinConfigs => Instance.PinConfigs;

    private static void Add(string name) {
        if (!PinConfigs.ContainsKey(name)) {
            PinConfigs[name] = new PinConfigModel();
        }
    }

    public static void Add(string name, PinoutModel pinout) {
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(name), new ArgumentNullException(nameof(name)), "name is null");
        DebugUtil.Assert(pinout != null, new ArgumentNullException(nameof(pinout)), "pinout is null");
        Add(name);
        PinConfigs[name!].Name.String    = name;
        PinConfigs[name].Position.String = pinout!.Position.ToString();
    }
}