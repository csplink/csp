using CSP.Events;
using CSP.Utils;
using CSP.Utils.Extensions;
using Prism.Mvvm;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.IO;
using System.Windows;
using System.Xml.Serialization;

// ReSharper disable UnusedAutoPropertyAccessor.Global

namespace CSP.Database.Models.MCU
{
    [XmlRoot("MCU", IsNullable = false)]
    public class MCUModel
    {
        [XmlArray("Applications")]
        [XmlArrayItem("Document")]
        public DocumentModel[] Applications { get; set; }

        [XmlAttribute]
        public string ClockTree { get; set; }

        [XmlAttribute]
        public string Company { get; set; }

        [XmlArray("DataSheets")]
        [XmlArrayItem("Document")]
        public DocumentModel[] DataSheets { get; set; }

        [XmlArray("Errata")]
        [XmlArrayItem("Document")]
        public DocumentModel[] Errata { get; set; }

        [XmlAttribute]
        public bool HasPowerPad { get; set; }

        public string Illustrate { get; set; }

        public string Introduction { get; set; }

        [XmlAttribute]
        public string IoType { get; set; }

        [XmlAttribute]
        public string Line { get; set; }

        [XmlArray("Modules")]
        [XmlArrayItem("Module")]
        public ModuleModel[] Modules { get; set; }

        [XmlAttribute]
        public string Name { get; set; }

        [XmlAttribute]
        public string Package { get; set; }

        [XmlArray("Pins")]
        [XmlArrayItem("Pin")]
        public PinModel[] Pins { get; set; }

        [XmlAttribute]
        public float Price { get; set; }

        [XmlArray("Programs")]
        [XmlArrayItem("Document")]
        public DocumentModel[] Programs { get; set; }

        [XmlArray("References")]
        [XmlArrayItem("Document")]
        public DocumentModel[] References { get; set; }

        [XmlAttribute]
        public string Series { get; set; }

        public string Url { get; set; }

        internal static MCUModel Load(string path)
        {
            DebugUtil.Assert(!path.IsNullOrEmpty(), new ArgumentNullException(nameof(path)));

            if (!File.Exists(path)) return null;

            var deserializer = new XmlSerializer(typeof(MCUModel));
            var reader = new StreamReader(path);

            MCUModel rtn;
            try
            {
                rtn = (MCUModel)deserializer.Deserialize(reader);
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
            // ReSharper disable once LoopCanBePartlyConvertedToQuery
            foreach (var pin in rtn.Pins)
            {
                if (pin.FunctionsTemp != null)
                {
                    foreach (var functions in pin.FunctionsTemp)
                    {
                        pin.Functions.Add(functions.Name, functions);
                    }
                }
            }

            return rtn;
        }

        public class DocumentModel
        {
            [XmlAttribute]
            public string Name { get; set; }

            public string Url { get; set; }
        }

        public class ModuleModel
        {
            [XmlArray("Categories")]
            [XmlArrayItem("Category")]
            public CategoryModel[] Categories { get; set; }

            [XmlAttribute]
            public string Name { get; set; }

            public class CategoryModel
            {
                [XmlAttribute]
                public string Name { get; set; }
            }
        }

        public class PinModel
        {
            private string _name;
            private int _position;

            public PinModel()
            {
                GPIOProperty.Data = new DataContextModel();
            }

            [XmlIgnore]
            public Dictionary<string, FunctionModel> Functions { get; } = new();

            [XmlArray("Functions")]
            [XmlArrayItem("Function")]
            public FunctionModel[] FunctionsTemp { get; set; }

            [XmlIgnore]
            public PropertyEvent.Model GPIOProperty { get; set; } = new();

            [XmlAttribute]
            public string Name
            {
                get => _name;
                set
                {
                    _name = value;
                    ((DataContextModel)GPIOProperty.Data).Name = value;
                }
            }

            [XmlAttribute]
            public int Position
            {
                get => _position;
                set
                {
                    _position = value;
                    ((DataContextModel)GPIOProperty.Data).Position = value;
                }
            }

            [XmlAttribute]
            public string Type { get; set; }

            public class DataContextModel : BindableBase
            {
                private string _function;
                private bool _isLocked;
                private string _label;
                private MapModel.EnumerateModel.ValuePropertyGridComboEditorModel _level = new();
                private MapModel.EnumerateModel.ValuePropertyGridComboEditorModel _mode = new();
                private string _name;
                private int _position;
                private MapModel.EnumerateModel.ValuePropertyGridComboEditorModel _pull = new();
                private MapModel.EnumerateModel.ValuePropertyGridComboEditorModel _speed = new();

                [Display(Name = "功能", Description = "GPIO 功能", GroupName = "系统")]
                [XmlAttribute]
                public string Function
                {
                    get => _function;
                    set => SetProperty(ref _function, value);
                }

                [Display(Name = "锁定", Description = "锁定", GroupName = "基础")]
                public bool IsLocked
                {
                    get => _isLocked;
                    set => SetProperty(ref _isLocked, value);
                }

                [Display(Name = "标签", Description = "GPIO 标签, 用于宏定义", GroupName = "基础")]
                public string Label
                {
                    get => _label;
                    set => SetProperty(ref _label, value);
                }

                [Display(Name = "电平", Description = "GPIO 电平", GroupName = "系统")]
                public MapModel.EnumerateModel.ValuePropertyGridComboEditorModel Level
                {
                    get => _level;
                    set => SetProperty(ref _level, value);
                }

                [Display(Name = "模式", Description = "GPIO 模式", GroupName = "系统")]
                public MapModel.EnumerateModel.ValuePropertyGridComboEditorModel Mode
                {
                    get => _mode;
                    set => SetProperty(ref _mode, value);
                }

                [ReadOnly(true)]
                [Display(Name = "名称", Description = "GPIO 名称", GroupName = "基础")]
                public string Name
                {
                    get => _name;
                    set => SetProperty(ref _name, value);
                }

                [ReadOnly(true)]
                [Display(Name = "引脚序号", Description = "GPIO 引脚序号", GroupName = "基础")]
                public int Position
                {
                    get => _position;
                    set => _ = SetProperty(ref _position, value);
                }

                [Display(Name = "上下拉", Description = "GPIO 上下拉", GroupName = "系统")]
                public MapModel.EnumerateModel.ValuePropertyGridComboEditorModel Pull
                {
                    get => _pull;
                    set => SetProperty(ref _pull, value);
                }

                [Display(Name = "速度", Description = "GPIO 速度", GroupName = "系统")]
                public MapModel.EnumerateModel.ValuePropertyGridComboEditorModel Speed
                {
                    get => _speed;
                    set => SetProperty(ref _speed, value);
                }
            }

            public class FunctionModel
            {
                [XmlIgnore]
                public IPModel.IpGpioModel.IpGpioModeModel Mode { get; set; }

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