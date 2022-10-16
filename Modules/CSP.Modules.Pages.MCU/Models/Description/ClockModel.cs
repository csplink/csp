using CSP.Utils;
using CSP.Utils.Extensions;
using Prism.Mvvm;
using System;
using System.Collections.Generic;
using System.IO;
using System.Windows;
using System.Xml.Serialization;

namespace CSP.Modules.Pages.MCU.Models.Description
{
    [XmlRoot("Clock", IsNullable = false)]
    public class ClockModel
    {
        [XmlIgnore]
        public Dictionary<string, ControlModel> ControlMap { get; set; } = new();

        [XmlArray("Controls")]
        [XmlArrayItem("Control")]
        public List<ControlModel> Controls { get; set; }

        [XmlIgnore]
        public Dictionary<int, EllipseModel> EllipseMap { get; set; } = new();

        [XmlArray("Ellipses")]
        [XmlArrayItem("Ellipse")]
        public List<EllipseModel> Ellipses { get; set; }

        [XmlAttribute]
        public float Height { get; set; }

        [XmlIgnore]
        public Dictionary<int, RectModel> RectMap { get; set; } = new();

        [XmlArray("Rects")]
        [XmlArrayItem("Rect")]
        public List<RectModel> Rects { get; set; }

        [XmlAttribute]
        public float Width { get; set; }

        internal static ClockModel Load(string path) {
            DebugUtil.Assert(!path.IsNullOrEmpty(), new ArgumentNullException(nameof(path)), "path不能为空");
            DebugUtil.Assert(File.Exists(path), new FileNotFoundException(nameof(path)), $"{path}: 不存在");

            if (path == null) return null;
            if (!File.Exists(path)) return null;

            var deserializer = new XmlSerializer(typeof(ClockModel));
            var reader = new StreamReader(path);

            ClockModel rtn;
            try {
                rtn = (ClockModel)deserializer.Deserialize(reader);
            }
            catch (InvalidOperationException e) {
                MessageBox.Show(e.Message, "错误", MessageBoxButton.OK, MessageBoxImage.Error);
                return null;
            }

            DebugUtil.Assert(rtn != null, new ArgumentNullException(nameof(rtn)), "XML反序列化失败");
            if (rtn == null)
                return null;

            //给辅助变量赋值,将变量转化为字典形式
            foreach (var rect in rtn.Rects) {
                rtn.RectMap.Add(rect.ID, rect);
            }
            foreach (var ellipse in rtn.Ellipses) {
                rtn.EllipseMap.Add(ellipse.ID, ellipse);
            }
            foreach (var control in rtn.Controls) {
                if (rtn.RectMap.ContainsKey(control.ID)) {
                    control.Height = rtn.RectMap[control.ID].Height;
                    control.Width = rtn.RectMap[control.ID].Width;
                    control.X = rtn.RectMap[control.ID].X;
                    control.Y = rtn.RectMap[control.ID].Y;
                }
                else if (rtn.EllipseMap.ContainsKey(control.ID)) {
                    control.Height = rtn.EllipseMap[control.ID].Height;
                    control.Width = rtn.EllipseMap[control.ID].Width;
                    control.X = rtn.EllipseMap[control.ID].X;
                    control.Y = rtn.EllipseMap[control.ID].Y;
                }
                rtn.ControlMap.Add(control.Name, control);
            }

            return rtn;
        }

        public class ControlModel : BindableBase
        {
            private float _displayValue;
            private float _value;

            [XmlAttribute]
            public int DefaultIndex { get; set; }

            [XmlAttribute]
            public float DefaultValue { get; set; }

            [XmlIgnore]
            public float DisplayValue {
                get => _displayValue;
                set {
                    if (!SetProperty(ref _displayValue, value))
                        return;

                    if (Multiple != 0)
                        Value = _displayValue * Multiple;
                }
            }

            [XmlAttribute]
            public string GroupName { get; set; }

            [XmlIgnore]
            public float Height { get; set; }

            [XmlAttribute]
            public int ID { get; set; }

            [XmlAttribute]
            public string Macro { get; set; }

            [XmlAttribute]
            public float Multiple { get; set; }

            [XmlAttribute]
            public string Name { get; set; }

            [XmlArray("Signals")]
            [XmlArrayItem("Signal")]
            public List<SignalModel> Signals { get; set; }

            [XmlArray("Status")]
            [XmlArrayItem("Status")]
            public List<StatusModel> Status { get; set; }

            [XmlAttribute]
            public string Type { get; set; }

            [XmlIgnore]
            public float Value {
                get => _value;
                set {
                    if (!SetProperty(ref _value, value))
                        return;
                    if (Multiple != 0)
                        DisplayValue = _value / Multiple;
                }
            }

            [XmlIgnore]
            public float Width { get; set; }

            [XmlIgnore]
            public float X { get; set; }

            [XmlIgnore]
            public float Y { get; set; }

            public class SignalModel
            {
                private string _dependencies;

                [XmlIgnore]
                public string[] DependenceArray { get; set; }

                public string Dependencies {
                    get => _dependencies;
                    set {
                        if (EqualityComparer<string>.Default.Equals(_dependencies, value))
                            return;
                        _dependencies = value;
                        DependenceArray = _dependencies.Split(";", StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
                    }
                }

                [XmlAttribute]
                public string Operator { get; set; } = "*";

                [XmlAttribute]
                public string Source { get; set; }

                [XmlAttribute]
                public float SourceValue { get; set; }

                [XmlIgnore]
                public string Text { get => Operator + Value; }

                [XmlAttribute]
                public float Value { get; set; } = 1;
            }

            public class StatusModel
            {
                private string _dependencies;

                [XmlIgnore]
                public string[] DependenceArray { get; set; }

                public string Dependencies {
                    get => _dependencies;
                    set {
                        if (EqualityComparer<string>.Default.Equals(_dependencies, value))
                            return;
                        _dependencies = value;
                        DependenceArray = _dependencies.Split(";", StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
                    }
                }

                [XmlAttribute]
                public bool IsEnable { get; set; }

                [XmlArray("Styles")]
                [XmlArrayItem("Style")]
                public List<StyleModel> Styles { get; set; }

                public class StyleModel
                {
                    [XmlAttribute]
                    public string Name { get; set; }

                    [XmlAttribute]
                    public string Value { get; set; }
                }
            }
        }

        public class EllipseModel
        {
            [XmlAttribute]
            public float Height { get; set; }

            [XmlAttribute]
            public int ID { get; set; }

            [XmlAttribute]
            public float Width { get; set; }

            [XmlAttribute]
            public float X { get; set; }

            [XmlAttribute]
            public float Y { get; set; }
        }

        public class RectModel
        {
            [XmlAttribute]
            public float Height { get; set; }

            [XmlAttribute]
            public int ID { get; set; }

            [XmlAttribute]
            public float Width { get; set; }

            [XmlAttribute]
            public float X { get; set; }

            [XmlAttribute]
            public float Y { get; set; }
        }
    }
}