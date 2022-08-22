using CSP.Models.Interfaces;
using CSP.Utils.Extensions;
using Prism.Ioc;
using Prism.Services.Dialogs;
using Serilog;
using System;
using System.Collections.Generic;

namespace CSP.Utils
{
    public static class DialogUtil
    {
        public static readonly List<string> DialogNames = new();
        public static readonly List<string> DialogWindowNames = new();

        public static void RegisterDialog<TView, TViewModel>(IContainerRegistry containerRegistry, string name = null) where TViewModel : IDialogWindowParameters {
            containerRegistry.RegisterDialog<TView, TViewModel>(name);

            AddDialogName(name);
        }

        public static void RegisterDialogWindow<TWindow>(IContainerRegistry containerRegistry, string name = null) where TWindow : IDialogWindow {
            containerRegistry.RegisterDialogWindow<TWindow>(name);

            AddDialogWindowName(name);
        }

        public static void ShowModalDialog(IDialogService dialogService, string name, IDialogParameters parameters = null, Action<IDialogResult> callback = null, string windowName = null) {
            Log.Information($"打开模态对话框 \"{name}\" + \"{windowName}\"");

            if (!windowName.IsNullOrEmpty()) {
                if (!DialogWindowNames.Contains(windowName)) {
                    var message = $"无Dialog Window \"{windowName}\"";
                    MessageBoxUtil.Error(message);
                }
            }

            if (DialogNames.Contains(name)) {
                dialogService.ShowDialog(name, parameters, callback, windowName);
            }
            else {
                var message = $"尝试打开模态对话框 \"{name}\" 失败";
                MessageBoxUtil.Error(message);
            }
        }

        public static void ShowNonModalDialog(IDialogService dialogService, string name, IDialogParameters parameters = null, Action<IDialogResult> callback = null, string windowName = null) {
            Log.Information($"打开非模态对话框 \"{name}\" + \"{windowName}\"");

            if (!windowName.IsNullOrEmpty()) {
                if (!DialogWindowNames.Contains(windowName)) {
                    var message = $"无Dialog Window \"{windowName}\"";
                    MessageBoxUtil.Error(message);
                }
            }

            if (DialogNames.Contains(name)) {
                dialogService.Show(name, parameters, callback, windowName);
            }
            else {
                var message = $"尝试打开非模态对话框 \"{name}\" 失败";
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
}