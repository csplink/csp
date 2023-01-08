﻿// Licensed under the Apache License, Version 2.0 (the "License");
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
// @file        IDialogWindowParameters.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using Prism.Services.Dialogs;
using System.Windows;

namespace CSP.Models.Interfaces
{
    public interface IDialogWindowParameters : IDialogAware
    {
        public double Height { get; }
        public double MinHeight { get; }
        public double MinWidth { get; }
        public bool ShowInTaskbar { get; }
        public SizeToContent SizeToContent { get; }
        public double Width { get; }
        public WindowState WindowState { get; set; }
    }
}