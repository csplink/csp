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
// @file        ConfigFile.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

namespace CSP.Resources;

public static class ConfigFile
{
    private static readonly ConfigFileInstance Config = new();

    public static string PathGit {
        get => Config.ReadKey("Path", "Git", Path.Git);
        set => Config.AddKey("Path", "Git", value);
    }

    public static string PathLogFile {
        get => Config.ReadKey("Path", "LogFile", Path.LogFile);
        set => Config.AddKey("Path", "LogFile", value);
    }

    public static string PathRepo {
        get => Config.ReadKey("Path", "Repo", Path.Repo);
        set => Config.AddKey("Path", "Repo", value);
    }

    public static void Save() {
        Config.Save();
    }
}