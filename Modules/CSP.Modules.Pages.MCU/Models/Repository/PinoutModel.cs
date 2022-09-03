using CSP.Utils;
using CSP.Utils.Extensions;
using System;
using System.Collections.Generic;
using System.IO;
using System.Windows;
using System.Xml.Serialization;

namespace CSP.Modules.Pages.MCU.Models.Repository
{
    [XmlRoot("Pinout", IsNullable = false)]
    public class PinoutModel
    {
        [XmlArray("Pins")]
        [XmlArrayItem("Pin")]
        public PinModel[] Pins { get; set; }

        internal static PinoutModel Load(string path) {
            DebugUtil.Assert(!path.IsNullOrEmpty(), new ArgumentNullException(nameof(path)), "path不能为空");
            DebugUtil.Assert(File.Exists(path), new FileNotFoundException(nameof(path)), $"{path}: 不存在");

            if (path == null) return null;
            if (!File.Exists(path)) return null;

            var deserializer = new XmlSerializer(typeof(PinoutModel));
            var reader = new StreamReader(path);

            PinoutModel rtn;
            try {
                rtn = (PinoutModel)deserializer.Deserialize(reader);
            }
            catch (InvalidOperationException e) {
                MessageBox.Show(e.Message, "错误", MessageBoxButton.OK, MessageBoxImage.Error);
                return null;
            }

            DebugUtil.Assert(rtn != null, new ArgumentNullException(nameof(rtn)), "XML反序列化失败");
            if (rtn == null)
                return null;

            //给辅助变量赋值,将变量转化为字典形式
            foreach (var pin in rtn.Pins) {
                if (pin.Functions != null) {
                    foreach (var functions in pin.Functions) {
                        pin.FunctionMap.Add(functions.Name, functions);
                    }
                }
            }

            return rtn;
        }

        public class PinModel
        {
            [XmlIgnore]
            public Dictionary<string, FunctionModel> FunctionMap { get; } = new();

            [XmlArray("Functions")]
            [XmlArrayItem("Function")]
            public FunctionModel[] Functions { get; set; }

            [XmlAttribute]
            public string Name { get; set; }

            [XmlAttribute]
            public int Position { get; set; }

            [XmlAttribute]
            public string Type { get; set; }

            public class FunctionModel
            {
                [XmlAttribute("Mode")]
                public string ModeName { get; set; }

                [XmlAttribute]
                public string Name { get; set; }

                [XmlAttribute]
                public string Type { get; set; }
            }

            public class ObjectModel
            {
                [XmlAttribute]
                public string Value { get; set; }
            }
        }
    }
}