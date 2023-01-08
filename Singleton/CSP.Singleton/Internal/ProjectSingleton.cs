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
// @file        ProjectSingleton.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System;
using System.Collections.Generic;
using CSP.Models.Internal;
using CSP.Utils;

namespace CSP.Singleton.Internal;

public static class ProjectSingleton
{
    private static readonly ProjectSingletonInstance Instance = ProjectSingletonInstance.Instance;

    public static ProjectModel Project => Instance.Project;

    public static void ChangeDefine(string oldKey, string newKey, string newValue) {
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(oldKey) || !string.IsNullOrWhiteSpace(newKey),
            new ArgumentNullException(nameof(oldKey) + " or " + nameof(newKey)), "oldKey 或者 newKey 不能均为空");

        if (oldKey != null) {
            oldKey = "CSP_USING_" + oldKey.ToUpper();
        }
        else {
            oldKey = "";
        }

        if (newKey != null) {
            newKey = "CSP_USING_" + newKey.ToUpper();
        }
        else {
            newKey = "";
        }

        if (Project.Defines.ContainsKey(oldKey!)) {
            Project.Defines.Remove(oldKey);
        }

        if (Project.Defines.ContainsKey(newKey!)) {
            Project.Defines.Remove(newKey);
        }

        Project.Defines.Add(newKey, newValue);
    }

    public static bool IsDependence(IEnumerable<string> dependencies) {
        if (dependencies == null) {
            return true;
        }

        bool isDependence = true;
        foreach (string dependence in dependencies) {
            if (!Project.Defines.ContainsKey("CSP_USING_" + dependence.ToUpper())) {
                isDependence = false;
            }
        }

        return isDependence;
    }
}