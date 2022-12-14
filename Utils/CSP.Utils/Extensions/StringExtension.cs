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
// @file        StringExtension.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace CSP.Utils.Extensions;

public static class StringExtension
{
    public static byte[] FromHexToByteArray(this string str) {
        if (str == null) {
            throw new ArgumentNullException(nameof(str));
        }

        string[] chars       = str.Replace(" ", "").Split(2);
        byte[]   returnBytes = new byte[chars.Length];

        //逐个字符变为16进制字节数据
        for (int i = 0; i < chars.Length; i++) {
            returnBytes[i] = Convert.ToByte(chars[i], 16);
        }

        return returnBytes;
    }

    public static string FromHexToText(this string str, Encoding encoding) {
        if (str == null) {
            throw new ArgumentNullException(nameof(str));
        }

        if (encoding == null) {
            throw new ArgumentNullException(nameof(encoding));
        }

        byte[] bytes = str.FromHexToByteArray();

        return encoding.GetString(bytes);
    }

    public static byte[] FromTextToByteArray(this string str, Encoding encoding) {
        if (str == null) {
            throw new ArgumentNullException(nameof(str));
        }

        if (encoding == null) {
            throw new ArgumentNullException(nameof(encoding));
        }

        return encoding.GetBytes(str);
    }

    public static string FromTextToHex(this string str, Encoding encoding) {
        if (str == null) {
            throw new ArgumentNullException(nameof(str));
        }

        if (encoding == null) {
            throw new ArgumentNullException(nameof(encoding));
        }

        return BitConverter.ToString(encoding.GetBytes(str)).Replace("-", " ");
    }

    public static bool IsLegalHex(this string str) {
        if (str == null) {
            throw new ArgumentNullException(nameof(str));
        }

        IList<char> hexSet = new List<char> {
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e', 'f'
        };

        return str.All(item => hexSet.Contains<char>(item));
    }

    /// <summary>
    ///     按指定长度分割字符串
    /// </summary>
    /// <param name="str">
    ///     原字符串
    /// </param>
    /// <param name="count">
    ///     分割长度
    /// </param>
    /// <returns>
    ///     被分割后的字符串
    /// </returns>
    public static string[] Split(this string str, int count) {
        if (str == null) {
            throw new ArgumentNullException(nameof(str));
        }

        List<string> list = new();

        for (int i = 0; i < str.Length; i += count) {
            list.Add(str.Length - i > count ? str.Substring(i, count) : str.Substring(i));
        }

        return list.ToArray();
    }
}