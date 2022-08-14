using CSP.Utils;
using CSP.Utils.Extensions;
using System;
using System.Collections.Generic;
using System.IO;
using System.Windows;
using System.Xml.Serialization;

// ReSharper disable UnusedAutoPropertyAccessor.Global

namespace CSP.Database.Models.MCU
{
    [XmlRoot("IP", IsNullable = false)]
    public class IPModel
    {
        public IpGpioModel GPIO { get; set; }

        internal static IPModel Load(string path)
        {
            DebugUtil.Assert(!path.IsNullOrEmpty(), new ArgumentNullException(nameof(path)));

            if (!File.Exists(path))
                return null;

            var deserializer = new XmlSerializer(typeof(IPModel));
            var reader = new StreamReader(path);

            IPModel rtn;
            try
            {
                rtn = (IPModel)deserializer.Deserialize(reader);
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
            foreach (var mode in rtn.GPIO.ModesTemp)
            {
                foreach (var parameter in mode.ParametersTemp)
                {
                    mode.Parameters.Add(parameter.Group, parameter);
                }

                rtn.GPIO.Modes.Add(mode.Name, mode);
            }

            return rtn;
        }

        public class IpGpioModel
        {
            [XmlIgnore]
            public Dictionary<string, IpGpioModeModel> Modes { get; } = new();

            [XmlArray("Modes")]
            [XmlArrayItem("Mode")]
            public IpGpioModeModel[] ModesTemp { get; set; }

            public class IpGpioModeModel
            {
                [XmlAttribute]
                public string Name { get; set; }

                [XmlIgnore]
                public Dictionary<string, IpGpioModeParameterModel> Parameters { get; } = new();

                [XmlArray("Parameters")]
                [XmlArrayItem("Parameter")]
                public IpGpioModeParameterModel[] ParametersTemp { get; set; }

                [XmlAttribute]
                public string Type { get; set; }

                public class IpGpioModeParameterModel
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
}