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
// @file        IsNullConverter.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System;
using System.Globalization;
using System.Windows.Data;

namespace CSP.Utils.Converter;

public class IsNullConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture) {
        return value == null;
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture) {
        DebugUtil.Assert(false, new InvalidOperationException("IsNullConverter can only be used OneWay."));

        return null;
    }
}