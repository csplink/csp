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

    public Dictionary<int, RectModel> Rects { get; set; }

    public Dictionary<int, EllipseModel> Ellipses { get; set; }

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

        return rtn;
    }

    public class ControlModel
    {
        public BaseModel Base { get; set; }

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
    }

    public class RectModel
    {
        public float X { get; set; }

        public float Y { get; set; }

        public float Width { get; set; }

        public float Height { get; set; }
    }

    public class EllipseModel
    {
        public float X { get; set; }

        public float Y { get; set; }

        public float Width { get; set; }

        public float Height { get; set; }
    }
}