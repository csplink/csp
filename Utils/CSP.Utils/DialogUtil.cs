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
// @file        DialogUtil.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System;
using System.Collections.Generic;
using CSP.Models.Interfaces;
using Prism.Ioc;
using Prism.Services.Dialogs;
using Serilog;

namespace CSP.Utils;

public static class DialogUtil
{
    public static readonly List<string> DialogNames       = new();
    public static readonly List<string> DialogWindowNames = new();

    public static void RegisterDialog<TView, TViewModel>(IContainerRegistry containerRegistry, string name = null)
        where TViewModel : IDialogWindowParameters {
        containerRegistry.RegisterDialog<TView, TViewModel>(name);

        AddDialogName(name);
    }

    public static void RegisterDialogWindow<TWindow>(IContainerRegistry containerRegistry, string name = null)
        where TWindow : IDialogWindow {
        containerRegistry.RegisterDialogWindow<TWindow>(name);

        AddDialogWindowName(name);
    }

    public static void ShowModalDialog(IDialogService dialogService,   string name, IDialogParameters parameters = null,
        Action<IDialogResult>                         callback = null, string windowName = null) {
        Log.Information($"打开模态对话框 \"{name}\" + \"{windowName}\"");

        if (!string.IsNullOrWhiteSpace(windowName)) {
            if (!DialogWindowNames.Contains(windowName)) {
                string message = $"无Dialog Window \"{windowName}\"";
                MessageBoxUtil.Error(message);
            }
        }

        if (DialogNames.Contains(name)) {
            dialogService.ShowDialog(name, parameters, callback, windowName);
        }
        else {
            string message = $"尝试打开模态对话框 \"{name}\" 失败";
            MessageBoxUtil.Error(message);
        }
    }

    public static void ShowNonModalDialog(IDialogService dialogService, string name,
        IDialogParameters parameters = null, Action<IDialogResult> callback = null, string windowName = null) {
        Log.Information($"打开非模态对话框 \"{name}\" + \"{windowName}\"");

        if (!string.IsNullOrWhiteSpace(windowName)) {
            if (!DialogWindowNames.Contains(windowName)) {
                string message = $"无Dialog Window \"{windowName}\"";
                MessageBoxUtil.Error(message);
            }
        }

        if (DialogNames.Contains(name)) {
            dialogService.Show(name, parameters, callback, windowName);
        }
        else {
            string message = $"尝试打开非模态对话框 \"{name}\" 失败";
            MessageBoxUtil.Error(message);
        }
    }

    private static void AddDialogName(string name) {
        DialogNames.Add(name);
    }

    private static void AddDialogWindowName(string name) {
        DialogWindowNames.Add(name);
    }
}