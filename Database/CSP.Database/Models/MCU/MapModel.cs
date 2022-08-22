using CSP.Utils;
using CSP.Utils.Extensions;
using Prism.Mvvm;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Text;
using System.Windows;
using System.Xml;
using System.Xml.Serialization;

// ReSharper disable UnusedAutoPropertyAccessor.Global

namespace CSP.Database.Models.MCU
{
    [XmlRoot("Map", IsNullable = false)]
    public class MapModel
    {
        [XmlIgnore]
        public Dictionary<string, Dictionary<string, Attribute>> Attributes { get; set; } = new();

        [XmlIgnore]
        public Dictionary<string, GroupModel> Groups { get; } = new();

        [XmlArray("Groups")]
        [XmlArrayItem("Group")]
        public GroupModel[] GroupsTemp { get; set; }

        [XmlArray("Properties")]
        [XmlArrayItem("Property")]
        public PropertyModel[] Properties { get; set; }

        [XmlIgnore]
        public Dictionary<string, string> Total { get; } = new();

        internal static void Create(string path, MapModel model) {
            DebugUtil.Assert(path != null, new ArgumentNullException(nameof(path)));
            DebugUtil.Assert(model != null, new ArgumentNullException(nameof(model)));

            var dir = Path.GetDirectoryName(path);
            if (!Directory.Exists(dir))
                if (dir != null)
                    Directory.CreateDirectory(dir);

            var serializer = new XmlSerializer(typeof(MapModel));
            // ReSharper disable once AssignNullToNotNullAttribute
            Stream fs = new FileStream(path, FileMode.Create);
            var writer = new XmlTextWriter(fs, Encoding.UTF8);
            writer.Formatting = Formatting.Indented;
            writer.Indentation = 4;

            serializer.Serialize(writer, model);
            writer.Close();
        }

        internal static MapModel Load(string path) {
            DebugUtil.Assert(!path.IsNullOrEmpty(), new ArgumentNullException(nameof(path)));

            if (!File.Exists(path)) return null;

            var deserializer = new XmlSerializer(typeof(MapModel));
            var reader = new StreamReader(path);

            MapModel rtn;
            try {
                rtn = (MapModel)deserializer.Deserialize(reader);
            }
            catch (InvalidOperationException e) {
                MessageBox.Show(e.Message, "错误", MessageBoxButton.OK, MessageBoxImage.Error);
                return null;
            }

            DebugUtil.Assert(rtn != null, new ArgumentNullException(nameof(rtn)), "XML反序列化失败");
            if (rtn == null)
                return null;

            //给辅助变量赋值,将变量转化为字典形式
            foreach (var group in rtn.GroupsTemp) {
                foreach (var value in group.ValuesTemp) {
                    rtn.Total.Add(value.Name, value.Comments);
                }

                rtn.Groups.Add(group.Name, group);
            }

            foreach (var property in rtn.Properties) {
                var attributes = new Dictionary<string, Attribute>
                {
                    {"DisplayName", new DisplayNameAttribute(property.DisplayName) },
                    {"Description", new DescriptionAttribute(property.Description) },
                    {"Category",new CategoryAttribute(property.Category) },
                    {"ReadOnly", new ReadOnlyAttribute(property.ReadOnly) }
                };
                rtn.Attributes.Add(property.Group, attributes);
            }

            return rtn;
        }

        internal static MapModel Transform(string path) {
            DebugUtil.Assert(!path.IsNullOrEmpty(), new ArgumentNullException(nameof(path)));

            if (!File.Exists(path)) return null;

            var map = new MapModel();
            var groups = new List<GroupModel>();

            StreamReader reader = new(path, Encoding.UTF8);

            // string line;
            // while ((line = reader.ReadLine()) != null)
            while (reader.ReadLine() is { } line) {
                if (!line.StartsWith(@"/** @defgroup ")) {
                    continue;
                }

                GroupModel group = null;
                var ps = line.Split(" ", StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
                if (ps.Length >= 4) {
                    group = new GroupModel { Name = ps[2], Comments = ps[3] };
                }

                var values = new List<GroupModel.ValueModel>();
                while ((line = reader.ReadLine()) != null) {
                    if (line.StartsWith(@"#define CHAL_") && line.Contains(@"  // ")) {
                        ps = line.Split(" ", StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
                        if (ps.Length >= 5) {
                            values.Add(new GroupModel.ValueModel { Name = ps[1], Comments = ps[4] });
                        }
                    }
                    else if (line.StartsWith(@" * @}")) {
                        if (group != null) {
                            group.ValuesTemp = values.ToArray();
                            groups.Add(group);
                        }
                        values.Clear();
                        break;
                    }
                }
            }

            reader.Close();
            map.GroupsTemp = groups.ToArray();
            return map;
        }

        public class GroupModel
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
                public string Value {
                    get => _value;
                    set => SetProperty(ref _value, value);
                }
            }
        }

        public class PropertyModel
        {
            public string Category { get; set; }

            public string Description { get; set; }

            public string DisplayName { get; set; }

            [XmlAttribute]
            public string Group { get; set; }

            public bool ReadOnly { get; set; }
        }
    }
}