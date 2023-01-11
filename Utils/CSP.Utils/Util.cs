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
// @file        Util.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-11     xqyjlj       add Cmd and Run
// 2023-01-08     xqyjlj       initial version
//

using System;
using System.Diagnostics;
using System.IO;
using Serilog;

namespace CSP.Utils;

public static class Util
{
    public static string Cmd(string arguments, string workingDirectory = "") {
        string error = "";
        using (Process process = new()) {
            process.StartInfo.FileName = "cmd";
            process.StartInfo.UseShellExecute = false;
            process.StartInfo.RedirectStandardInput = true;
            process.StartInfo.RedirectStandardOutput = false;
            process.StartInfo.RedirectStandardError = false;
            process.StartInfo.CreateNoWindow = true;
            process.StartInfo.WorkingDirectory = workingDirectory;
            try {
                process.Start();
                process.StandardInput.WriteLine(arguments);
                process.StandardInput.AutoFlush = true;
                process.WaitForExit();
            }
            catch (Exception e) {
                error = e.Message;
                Log.Error(error);
            }
        }

        return error;
    }

    public static (string, string, string) Run(string exec, string arguments, string workingDirectory = "") {
        string stdOutput = "";
        string stdError = "";
        string error = "";
        using (Process process = new()) {
            process.StartInfo.FileName = exec;
            process.StartInfo.UseShellExecute = false;
            process.StartInfo.RedirectStandardInput = true;
            process.StartInfo.RedirectStandardOutput = true;
            process.StartInfo.RedirectStandardError = true;
            process.StartInfo.CreateNoWindow = true;
            process.StartInfo.Arguments = arguments;
            process.StartInfo.WorkingDirectory = workingDirectory;
            try {
                process.Start();
                process.StandardInput.WriteLine(arguments);
                process.StandardInput.AutoFlush = true;
                StreamReader standardOutput = process.StandardOutput;
                StreamReader standardError = process.StandardError;
                stdOutput = standardOutput.ReadToEnd();
                stdError = standardError.ReadToEnd();
                process.WaitForExit();
            }
            catch (Exception e) {
                error = e.Message;
                Log.Error(error);
            }
        }

        return (stdOutput, stdError, error);
    }

    public static void OpenUrl(string url) {
        if (string.IsNullOrWhiteSpace(url)) {
            return;
        }

        Cmd($"start {url}&exit");
    }
}