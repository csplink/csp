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
// @file        ClockModel.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System;
using System.Collections.Generic;
using System.IO;
using System.Windows;
using CSP.Utils;
using Prism.Mvvm;
using YamlDotNet.Serialization;

namespace CSP.Models.HAL.Config;

public class ClockModel
{
    public float Width { get; set; }

    public float Height { get; set; }

    public Dictionary<int, ControlModel> Controls { get; set; }

    public Dictionary<int, ShapeModel> Rects { get; set; }

    public Dictionary<int, ShapeModel> Ellipses { get; set; }

    [YamlIgnore]
    public Dictionary<int, ShapeModel> Shapes { get; } = new();

    public static ClockModel Load(string path) {
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(path), new ArgumentNullException(nameof(path)));

        if (!File.Exists(path)) {
            return null;
        }

        Deserializer deserializer = new();

        ClockModel rtn;
        try {
            using (StreamReader reader = new(path)) {
                rtn = deserializer.Deserialize<ClockModel>(reader);
            }
        }
        catch (InvalidOperationException e) {
            MessageBox.Show(e.Message, "error", MessageBoxButton.OK, MessageBoxImage.Error);

            return null;
        }

        DebugUtil.Assert(rtn != null, new ArgumentNullException("Clock.YAML"), "YAML deserialization failed");

        foreach (var (id, shape) in rtn!.Rects) {
            rtn.Shapes.Add(id, shape);
        }

        foreach (var (id, shape) in rtn!.Ellipses) {
            rtn.Shapes.Add(id, shape);
        }

        return rtn;
    }

    public int FindIDByName(string name) {
        foreach (var (controlID, control) in Controls) {
            if (name == control.Base.Name) {
                return controlID;
            }
        }

        return -1;
    }

    public class ControlModel : BindableBase
    {
        private float _displayValue;
        private float _value;

        [YamlIgnore]
        public float DisplayValue {
            get => _displayValue;
            set {
                if (!SetProperty(ref _displayValue, value)) {
                    return;
                }

                if (Base.Multiple != 0) {
                    Value = _displayValue * Base.Multiple;
                }
            }
        }

        public float DefaultValue { get; set; }

        public BaseModel Base { get; set; }

        public Dictionary<string, StyleModel> Styles { get; set; }

        public SignalModel[] Signals { get; set; }

        [YamlIgnore]
        public float Value {
            get => _value;
            set {
                if (!SetProperty(ref _value, value)) {
                    return;
                }

                if (Base.Multiple != 0) {
                    DisplayValue = _value / Base.Multiple;
                }
            }
        }

        public class BaseModel
        {
            public string Name { get; set; }

            public string Type { get; set; }

            public int Multiple { get; set; }

            public float DefaultValue { get; set; }

            public int DefaultIndex { get; set; }

            public string GroupName { get; set; }

            public string Macro { get; set; }

            public bool IsChecked { get; set; }
        }

        public class StyleModel
        {
            public bool IsEnabled { get; set; }

            public string[] Dependencies { get; set; }

            public Dictionary<string, string> Text { get; set; }

            public string Status { get; set; }
        }

        public class SignalModel
        {
            public string Operator { get; set; } = "*";

            public float Value { get; set; } = 1;

            public string[] Dependencies { get; set; }

            public string Source { get; set; }

            public float SourceValue { get; set; }

            public string Text => Operator + Value;
        }
    }

    public class ShapeModel
    {
        public float X { get; set; }

        public float Y { get; set; }

        public float Width { get; set; }

        public float Height { get; set; }
    }
}