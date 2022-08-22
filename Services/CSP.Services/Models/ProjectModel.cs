using CSP.Utils;
using Prism.Mvvm;
using System;
using System.IO;
using System.Windows;
using System.Xml.Serialization;

namespace CSP.Services.Models
{
    [XmlRoot("Project", IsNullable = false)]
    public class ProjectModel : BindableBase
    {
        [XmlElement(ElementName = "Header")]
        public string Header { get; set; }

        [XmlElement("Target")]
        public TargetModel Target { get; set; }

        [XmlElement(ElementName = "Version")]
        public string Version { get; set; }

        internal static void Create(string path, ProjectModel model) {
            DebugUtil.Assert(path != null, new ArgumentNullException(nameof(path)));
            DebugUtil.Assert(model != null, new ArgumentNullException(nameof(model)));

            var dir = Path.GetDirectoryName(path);
            if (!Directory.Exists(dir))
                if (dir != null)
                    Directory.CreateDirectory(dir);

            var serializer = new XmlSerializer(typeof(ProjectModel));
            // ReSharper disable once AssignNullToNotNullAttribute
            Stream fs = new FileStream(path, FileMode.Create);
            var writer = new StreamWriter(fs);

            // var ns = new XmlSerializerNamespaces();
            // ns.Add("xsi", "http://www.w3.org/2001/XMLSchema-instance");
            // serializer.Serialize(writer, prj, ns);

            serializer.Serialize(writer, model);
            writer.Close();
        }

        internal static ProjectModel Load(string path) {
            DebugUtil.Assert(path != null, new ArgumentNullException(nameof(path)));

            if (!File.Exists(path)) return null;

            var deserializer = new XmlSerializer(typeof(ProjectModel));
            var reader = new StreamReader(path);

            ProjectModel rtn;
            try {
                rtn = (ProjectModel)deserializer.Deserialize(reader);
            }
            catch (InvalidOperationException e) {
                MessageBox.Show(e.Message, "错误", MessageBoxButton.OK, MessageBoxImage.Error);
                return null;
            }

            DebugUtil.Assert(rtn != null, new ArgumentNullException(nameof(rtn)), "XML反序列化失败");

            return rtn;
        }

        public class TargetModel : BindableBase
        {
            [XmlElement("MCU")]
            public MCUModel MCU { get; set; }

            [XmlAttribute("Name")]
            public string Name { get; set; }

            [XmlAttribute("Type")]
            public string Type { get; set; }

            public class MCUModel : BindableBase
            {
                [XmlAttribute("Company")]
                public string Company { get; set; }

                [XmlAttribute("Name")]
                public string Name { get; set; }
            }
        }
    }
}