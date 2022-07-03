using CSP.Utils.Extensions;
using Prism.Mvvm;
using Serilog;
using System;
using System.IO;
using System.Windows;
using System.Xml.Serialization;

// ReSharper disable UnusedAutoPropertyAccessor.Global

namespace CSP.Database.Models.MCU
{
    [XmlRoot("Repository", IsNullable = false)]
    public class RepositoryModel
    {
        [XmlArray("Companies")]
        [XmlArrayItem("Company")]
        public CompanyModel[] Companies { get; set; }

        internal static RepositoryModel Load(string path)
        {
            if (path.IsNullOrEmpty())
                Log.Error(new ArgumentNullException(nameof(path)), $"路径 \"{path}\" 不存在");

            if (!File.Exists(path))
                return null;

            var deserializer = new XmlSerializer(typeof(RepositoryModel));
            var reader = new StreamReader(path);
            RepositoryModel rtn;
            try
            {
                rtn = (RepositoryModel)deserializer.Deserialize(reader);
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

            // 补充辅助值

            foreach (var company in rtn.Companies)
            {
                foreach (var series in company.Series)
                {
                    foreach (var line in series.Lines)
                    {
                        foreach (var mcu in line.MCU)
                        {
                            mcu.Company = company.Name;
                            mcu.Series = series.Name;
                            mcu.Line = line.Name;

                            //TODO 需要在此处加入价格表数据更新
                        }
                    }
                }
            }

            return rtn;
        }

        public class CompanyModel
        {
            [XmlAttribute("Name")]
            public string Name { get; set; }

            [XmlArray("Series")]
            [XmlArrayItem("Series")]
            public SeriesModel[] Series { get; set; }

            public class SeriesModel
            {
                [XmlArray("Lines")]
                [XmlArrayItem("Line")]
                public LineModel[] Lines { get; set; }

                [XmlAttribute("Name")]
                public string Name { get; set; }

                public class LineModel
                {
                    [XmlArray("MCU")]
                    [XmlArrayItem("MCU")]
                    public MCUModel[] MCU { get; set; }

                    [XmlAttribute("Name")]
                    public string Name { get; set; }

                    public class MCUModel
                    {
                        [XmlIgnore]
                        public string Company { get; set; }

                        [XmlAttribute("Core")]
                        public string Core { get; set; }

                        [XmlElement("Current")]
                        public CurrentModel Current { get; set; }

                        [XmlAttribute("Flash")]
                        public float Flash { get; set; }

                        [XmlAttribute("Frequency")]
                        public float Frequency { get; set; }

                        [XmlAttribute("IO")]
                        public int IO { get; set; }

                        [XmlIgnore]
                        public string Line { get; set; }

                        [XmlAttribute("Name")]
                        public string Name { get; set; }

                        [XmlAttribute("Package")]
                        public string Package { get; set; }

                        [XmlArray("Peripherals")]
                        [XmlArrayItem("Peripheral")]
                        public PeripheralModel[] Peripherals { get; set; }

                        [XmlIgnore]
                        public float Price { get; set; }

                        [XmlAttribute("Ram")]
                        public float Ram { get; set; }

                        [XmlIgnore]
                        public string Series { get; set; }

                        [XmlElement("Temperature")]
                        public TemperatureModel Temperature { get; set; }

                        [XmlElement("Voltage")]
                        public VoltageModel Voltage { get; set; }

                        public class CurrentModel
                        {
                            [XmlAttribute("Lowest")]
                            public float Lowest { get; set; }

                            [XmlAttribute("Run")]
                            public float Run { get; set; }
                        }

                        public class PeripheralModel
                        {
                            [XmlAttribute("Number")]
                            public int Number { get; set; }

                            [XmlAttribute("Type")]
                            public string Type { get; set; }
                        }

                        public class TemperatureModel : BindableBase
                        {
                            [XmlAttribute("Max")]
                            public float Max { get; set; }

                            [XmlAttribute("Min")]
                            public float Min { get; set; }
                        }

                        public class VoltageModel : BindableBase
                        {
                            [XmlAttribute("Max")]
                            public float Max { get; set; }

                            [XmlAttribute("Min")]
                            public float Min { get; set; }
                        }
                    }
                }
            }
        }
    }
}