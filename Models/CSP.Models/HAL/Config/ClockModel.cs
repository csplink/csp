using System;
using System.Collections.Generic;
using System.IO;
using System.Windows;
using CSP.Utils;
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

    public class ControlModel
    {
        [YamlIgnore]
        public float DisplayValue { get; set; }

        public float DefaultValue { get; set; }

        public BaseModel Base { get; set; }

        public Dictionary<string, StyleModel> Styles { get; set; }

        public SignalModel[] Signals { get; set; }

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
            public string Operator { get; set; }

            public float Value { get; set; }

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