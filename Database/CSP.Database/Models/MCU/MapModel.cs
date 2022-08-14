using CSP.Utils;
using CSP.Utils.Extensions;
using Prism.Mvvm;
using System;
using System.Collections.Generic;
using System.IO;
using System.Windows;
using System.Xml.Serialization;

// ReSharper disable UnusedAutoPropertyAccessor.Global

namespace CSP.Database.Models.MCU
{
    [XmlRoot("Map", IsNullable = false)]
    public class MapModel
    {
        [XmlIgnore]
        public Dictionary<string, EnumerateModel> Enumerate { get; } = new();

        [XmlArray("Enumerate")]
        [XmlArrayItem("Enumerate")]
        public EnumerateModel[] EnumerateTemp { get; set; }

        [XmlIgnore]
        public Dictionary<string, string> Total { get; } = new();

        internal static MapModel Load(string path)
        {
            DebugUtil.Assert(!path.IsNullOrEmpty(), new ArgumentNullException(nameof(path)));

            if (!File.Exists(path)) return null;

            var deserializer = new XmlSerializer(typeof(MapModel));
            var reader = new StreamReader(path);

            MapModel rtn;
            try
            {
                rtn = (MapModel)deserializer.Deserialize(reader);
            }
            catch (InvalidOperationException e)
            {
                MessageBox.Show(e.Message, "错误", MessageBoxButton.OK, MessageBoxImage.Error);
                return null;
            }

            DebugUtil.Assert(rtn != null, new ArgumentNullException(nameof(rtn)), "XML反序列化失败");
            if (rtn == null)
                return null;

            //给辅助变量赋值,将变量转化为字典形式
            foreach (var enumerate in rtn.EnumerateTemp)
            {
                foreach (var value in enumerate.ValuesTemp)
                {
                    rtn.Total.Add(value.Name, value.Comments);
                }

                rtn.Enumerate.Add(enumerate.Name, enumerate);
            }

            return rtn;
        }

        internal static MapModel Transform(string path)
        {
            var map = new MapModel();

            return map;
        }

        public class EnumerateModel
        {
            public string Comments { get; set; }

            [XmlAttribute]
            public string Name { get; set; }

            [XmlIgnore]
            public Dictionary<string, string> Values { get; } = new();

            [XmlArray("Values")]
            [XmlArrayItem("Value")]
            public ValueModel[] ValuesTemp { get; set; }

            public class ValueModel
            {
                public string Comments { get; set; }

                [XmlAttribute]
                public string Name { get; set; }
            }

            public class ValuePropertyGridComboEditorModel : BindableBase
            {
                private string _value;

                [XmlIgnore]
                public Dictionary<string, string> Source { get; set; } = new();

                [XmlAttribute]
                public string Value
                {
                    get => _value;
                    set => SetProperty(ref _value, value);
                }
            }
        }
    }
}