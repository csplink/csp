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
// @file        SummarySingleton.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using CSP.Models.DB.Chip;

namespace CSP.Singleton.DB.Chip;

public static class SummarySingleton
{
    private static readonly SummarySingletonInstance Instance = SummarySingletonInstance.Instance;

    public static SummaryModel Summary => Instance.Summary;


    public static bool Set(string path) {
        Instance.Summary = SummaryModel.Load(path);

        return Instance.Summary != null;
    }
}