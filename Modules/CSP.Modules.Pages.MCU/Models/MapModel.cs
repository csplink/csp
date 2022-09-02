using CSP.Utils;
using CSP.Utils.Extensions;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Windows;
using System.Xml.Serialization;

namespace CSP.Modules.Pages.MCU.Models
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

        internal static MapModel Load(string path) {
            DebugUtil.Assert(!path.IsNullOrEmpty(), new ArgumentNullException(nameof(path)), "path不能为空");

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