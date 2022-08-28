using CSP.Utils;
using CSP.Utils.Extensions;
using System;
using System.IO;
using System.Windows;
using System.Xml.Serialization;

namespace CSP.Modules.Dialogs.NewMCU.Models
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

        public string CompanyUrl { get; set; }

        [XmlArray("DataSheets")]
        [XmlArrayItem("Document")]
        public DocumentModel[] DataSheets { get; set; }

        [XmlArray("Errata")]
        [XmlArrayItem("Document")]
        public DocumentModel[] Errata { get; set; }

        public HALModel HAL { get; set; }

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

        [XmlAttribute]
        public float Price { get; set; }

        [XmlArray("Programs")]
        [XmlArrayItem("Document")]
        public DocumentModel[] Programs { get; set; }

        [XmlArray("References")]
        [XmlArrayItem("Document")]
        public DocumentModel[] References { get; set; }

        public string RepositoryUrl { get; set; }

        [XmlAttribute]
        public string Series { get; set; }

        public string Url { get; set; }

        public static MCUModel Load(string path) {
            DebugUtil.Assert(!path.IsNullOrEmpty(), new ArgumentNullException(nameof(path)));

            if (!File.Exists(path)) return null;

            var deserializer = new XmlSerializer(typeof(MCUModel));
            var reader = new StreamReader(path);

            MCUModel rtn;
            try {
                rtn = (MCUModel)deserializer.Deserialize(reader);
            }
            catch (InvalidOperationException e) {
                MessageBox.Show(e.Message, "错误", MessageBoxButton.OK, MessageBoxImage.Error);
                return null;
            }

            DebugUtil.Assert(rtn != null, new ArgumentNullException(nameof(rtn)), "XML反序列化失败");
            return rtn;
        }

        public class DocumentModel
        {
            [XmlAttribute]
            public string Name { get; set; }

            public string Url { get; set; }
        }

        public class HALModel
        {
            [XmlAttribute]
            public string Name { get; set; }

            [XmlAttribute]
            public string Version { get; set; }
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
    }
}