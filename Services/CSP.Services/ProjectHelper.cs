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
// @file        ProjectHelper.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using CSP.Services.Models;
using CSP.Utils;
using System;

namespace CSP.Services
{
    public static class ProjectHelper
    {
        private static readonly ProjectInstance Instance = ProjectInstance.Instance;
        public static string Name { get; set; }
        public static string Path { get; set; }
        public static ProjectModel Project { get; set; }

        public static void Create(string path, ProjectModel model) {
            DebugUtil.Assert(path != null, new ArgumentNullException(nameof(path)));
            DebugUtil.Assert(model != null, new ArgumentNullException(nameof(model)));

            Path = path;
            Name = System.IO.Path.GetFileNameWithoutExtension(path);
            ProjectModel.Create(path, model);
            Project = model;
        }

        public static void Create(string path) {
            Create(path, Project);
        }

        public static ProjectModel Load(string path) {
            DebugUtil.Assert(path != null, new ArgumentNullException(nameof(path)));

            Path = path;
            Name = System.IO.Path.GetFileNameWithoutExtension(path);
            Project = ProjectModel.Load(path);
            return Project;
        }
    }
}