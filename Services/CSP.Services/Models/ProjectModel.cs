using CSP.Utils.Extensions;
using Prism.Mvvm;
using Serilog;
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

        internal static void Create(string path, ProjectModel model)
        {
            if (path == null)
                Log.Error(new ArgumentNullException(nameof(path)), "path 为 NULL");

            if (model == null)
                Log.Error(new ArgumentNullException(nameof(model)), "ProjectModel 为 NULL");

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

        internal static ProjectModel Load(string path)
        {
            if (path.IsNullOrEmpty())
                Log.Error(new ArgumentNullException(nameof(path)), $"路径 \"{path}\" 不存在");

            if (!File.Exists(path)) return null;

            var deserializer = new XmlSerializer(typeof(ProjectModel));
            var reader = new StreamReader(path);

            ProjectModel rtn;
            try
            {
                rtn = (ProjectModel)deserializer.Deserialize(reader);
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