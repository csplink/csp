using CSP.Utils;
using CSP.Utils.Extensions;
using System;
using System.Collections.Generic;
using System.IO;
using System.Windows;
using System.Xml.Serialization;

namespace CSP.Modules.Pages.MCU.Models.Repository
{
    [XmlRoot("IP", IsNullable = false)]
    public class IPModel
    {
        [XmlIgnore]
        public Dictionary<string, ModeModel> ModeMap { get; } = new();

        [XmlArray("Modes")]
        [XmlArrayItem("Mode")]
        public ModeModel[] Modes { get; set; }

        internal static IPModel Load(string path) {
            DebugUtil.Assert(!path.IsNullOrEmpty(), new ArgumentNullException(nameof(path)), "path不能为空");
            DebugUtil.Assert(File.Exists(path), new FileNotFoundException(nameof(path)), $"{path}: 不存在");

            if (path == null) return null;
            if (!File.Exists(path)) return null;

            var deserializer = new XmlSerializer(typeof(IPModel));
            var reader = new StreamReader(path);

            IPModel rtn;
            try {
                rtn = (IPModel)deserializer.Deserialize(reader);
            }
            catch (InvalidOperationException e) {
                MessageBox.Show(e.Message, "错误", MessageBoxButton.OK, MessageBoxImage.Error);
                return null;
            }

            DebugUtil.Assert(rtn != null, new ArgumentNullException(nameof(rtn)), "XML反序列化失败");
            if (rtn == null)
                return null;

            //给辅助变量赋值,将变量转化为字典形式
            foreach (var mode in rtn.Modes) {
                foreach (var parameter in mode.ParametersTemp) {
                    mode.Parameters.Add(parameter.Group, parameter);
                }

                rtn.ModeMap.Add(mode.Name, mode);
            }

            return rtn;
        }

        public class ModeModel
        {
            [XmlAttribute]
            public string Name { get; set; }

            [XmlIgnore]
            public Dictionary<string, ParameterModel> Parameters { get; } = new();

            [XmlArray("Parameters")]
            [XmlArrayItem("Parameter")]
            public ParameterModel[] ParametersTemp { get; set; }

            [XmlAttribute]
            public string Type { get; set; }

            public class ParameterModel
            {
                [XmlAttribute]
                public string Group { get; set; }

                [XmlArray("Values")]
                [XmlArrayItem("Value")]
                public string[] Values { get; set; }
            }
        }
    }
}