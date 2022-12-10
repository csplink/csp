﻿using System;
using System.IO;
using System.Windows;
using System.Xml.Serialization;
using CSP.Utils;
using CSP.Utils.Extensions;
using Prism.Mvvm;

namespace CSP.Modules.Dialogs.NewMCU.Models;

[XmlRoot("Repository", IsNullable = false)]
public class RepositoryModel
{
    [XmlArray("Companies")]
    [XmlArrayItem("Company")]
    public CompanyModel[] Companies { get; set; }

    public static RepositoryModel Load(string path) {
        DebugUtil.Assert(!path.IsNullOrEmpty(), new ArgumentNullException(nameof(path)), "path不能为空");
        DebugUtil.Assert(File.Exists(path), new FileNotFoundException(nameof(path)), $"{path}: 不存在");

        if (path == null) {
            return null;
        }

        if (!File.Exists(path)) {
            return null;
        }

        XmlSerializer   deserializer = new XmlSerializer(typeof(RepositoryModel));
        StreamReader    reader       = new StreamReader(path);
        RepositoryModel rtn;
        try {
            rtn = (RepositoryModel)deserializer.Deserialize(reader);
        }
        catch (InvalidOperationException e) {
            MessageBox.Show(e.Message, "错误", MessageBoxButton.OK, MessageBoxImage.Error);

            return null;
        }

        DebugUtil.Assert(rtn != null, new ArgumentNullException(nameof(rtn)), "XML反序列化失败");
        if (rtn == null) {
            return null;
        }

        // 补充辅助值
        foreach (CompanyModel company in rtn.Companies) {
            foreach (CompanyModel.SeriesModel series in company.Series) {
                foreach (CompanyModel.SeriesModel.LineModel line in series.Lines) {
                    foreach (CompanyModel.SeriesModel.LineModel.MCUModel mcu in line.MCU) {
                        mcu.Company = company.Name;
                        mcu.Series  = series.Name;
                        mcu.Line    = line.Name;

                        //TODO 需要在此处加入价格表数据更新
                    }
                }
            }
        }

        return rtn;
    }

    public class CompanyModel
    {
        [XmlAttribute] public string Name { get; set; }

        [XmlArray("Series")]
        [XmlArrayItem("Series")]
        public SeriesModel[] Series { get; set; }

        public class SeriesModel
        {
            [XmlArray("Lines")]
            [XmlArrayItem("Line")]
            public LineModel[] Lines { get; set; }

            [XmlAttribute] public string Name { get; set; }

            public class LineModel
            {
                [XmlArray("MCU")]
                [XmlArrayItem("MCU")]
                public MCUModel[] MCU { get; set; }

                [XmlAttribute] public string Name { get; set; }

                public class MCUModel
                {
                    [XmlIgnore] public string Company { get; set; }

                    [XmlAttribute] public string Core { get; set; }

                    public CurrentModel Current { get; set; }

                    [XmlAttribute] public float Flash { get; set; }

                    [XmlAttribute] public float Frequency { get; set; }

                    [XmlAttribute] public int IO { get; set; }

                    [XmlIgnore] public string Line { get; set; }

                    [XmlAttribute] public string Name { get; set; }

                    [XmlAttribute] public string Package { get; set; }

                    [XmlArray("Peripherals")]
                    [XmlArrayItem("Peripheral")]
                    public PeripheralModel[] Peripherals { get; set; }

                    [XmlIgnore] public float Price { get; set; }

                    [XmlAttribute] public float Ram { get; set; }

                    [XmlIgnore] public string Series { get; set; }

                    public TemperatureModel Temperature { get; set; }

                    public VoltageModel Voltage { get; set; }

                    public class CurrentModel
                    {
                        [XmlAttribute] public float Lowest { get; set; }

                        [XmlAttribute] public float Run { get; set; }
                    }

                    public class PeripheralModel
                    {
                        [XmlAttribute] public int Number { get; set; }

                        [XmlAttribute] public string Type { get; set; }
                    }

                    public class TemperatureModel : BindableBase
                    {
                        [XmlAttribute] public float Max { get; set; }

                        [XmlAttribute] public float Min { get; set; }
                    }

                    public class VoltageModel : BindableBase
                    {
                        [XmlAttribute] public float Max { get; set; }

                        [XmlAttribute] public float Min { get; set; }
                    }
                }
            }
        }
    }
}