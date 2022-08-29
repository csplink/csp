using CSP.Utils;
using CSP.Utils.Extensions;
using System;
using System.Collections.Generic;
using System.IO;
using System.Windows;
using System.Xml.Serialization;

namespace CSP.Modules.Pages.MCU.Models
{
    [XmlRoot("MCU", IsNullable = false)]
    public class PinoutsModel
    {
        [XmlArray("Pins")]
        [XmlArrayItem("Pin")]
        public PinModel[] Pins { get; set; }

        internal static PinoutsModel Load(string path) {
            DebugUtil.Assert(!path.IsNullOrEmpty(), new ArgumentNullException(nameof(path)));

            if (!File.Exists(path)) return null;

            var deserializer = new XmlSerializer(typeof(PinoutsModel));
            var reader = new StreamReader(path);

            PinoutsModel rtn;
            try {
                rtn = (PinoutsModel)deserializer.Deserialize(reader);
            }
            catch (InvalidOperationException e) {
                MessageBox.Show(e.Message, "错误", MessageBoxButton.OK, MessageBoxImage.Error);
                return null;
            }

            DebugUtil.Assert(rtn != null, new ArgumentNullException(nameof(rtn)), "XML反序列化失败");
            if (rtn == null)
                return null;

            //给辅助变量赋值,将变量转化为字典形式
            // ReSharper disable once LoopCanBePartlyConvertedToQuery
            foreach (var pin in rtn.Pins) {
                if (pin.FunctionsTemp != null) {
                    foreach (var functions in pin.FunctionsTemp) {
                        pin.Functions.Add(functions.Name, functions);
                    }
                }
            }

            return rtn;
        }

        public class PinModel
        {
            [XmlIgnore]
            public Dictionary<string, FunctionModel> Functions { get; } = new();

            [XmlArray("Functions")]
            [XmlArrayItem("Function")]
            public FunctionModel[] FunctionsTemp { get; set; }

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