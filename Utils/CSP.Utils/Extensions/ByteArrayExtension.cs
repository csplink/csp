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
// @file        ByteArrayExtension.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System;
using System.Text;

namespace CSP.Utils.Extensions;

public static class ByteArrayExtension
{
    public static string FromHexToString(this byte[] bytes) {
        StringBuilder builder = new StringBuilder();

        foreach (byte t in bytes) {
            builder.Append($"{t:X2} ");
        }

        return builder.ToString().Trim();
    }

    public static string FromTextToString(this byte[] bytes, Encoding encoding) {
        if (bytes == null) {
            throw new ArgumentNullException(nameof(bytes));
        }

        if (encoding == null) {
            throw new ArgumentNullException(nameof(encoding));
        }

        return encoding.GetString(bytes);
    }
}