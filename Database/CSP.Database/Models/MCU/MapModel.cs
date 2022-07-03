using CSP.Utils.Extensions;
using Prism.Mvvm;
using Serilog;
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
            if (path.IsNullOrEmpty())
                Log.Error(new ArgumentNullException(nameof(path)), $"路径 \"{path}\" 不存在");

            if (!File.Exists(path)) return null;

            var deserializer = new XmlSerializer(typeof(MapModel));
            var reader = new StreamReader(path);

            MapModel rtn;
            try
            {
                rtn = (MapModel)deserializer.Deserialize(reader);
                if (rtn == null)
                {
                    Log.Error(new ArgumentNullException(nameof(rtn)), "XML反序列化失败");
                    return null;
                }
            }
            catch (InvalidOperationException e)
            {
                MessageBox.Show(e.Message, "错误", MessageBoxButton.OK, MessageBoxImage.Error);
                return null;
            }

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

        public class EnumerateModel
        {
            [XmlElement("Comments")]
            public string Comments { get; set; }

            [XmlAttribute("Name")]
            public string Name { get; set; }

            [XmlIgnore]
            public Dictionary<string, string> Values { get; } = new();

            [XmlArray("Values")]
            [XmlArrayItem("Value")]
            public ValueModel[] ValuesTemp { get; set; }

            public class ValueModel
            {
                [XmlElement("Comments")]
                public string Comments { get; set; }

                [XmlAttribute("Name")]
                public string Name { get; set; }
            }

            public class ValuePropertyGridComboEditorModel : BindableBase
            {
                private string _value;

                [XmlIgnore]
                public Dictionary<string, string> Source { get; set; } = new();

                [XmlAttribute("Value")]
                public string Value
                {
                    get => _value;
                    set => SetProperty(ref _value, value);
                }
            }
        }
    }
}