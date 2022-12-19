using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Windows;
using CSP.Utils;
using YamlDotNet.Serialization;

namespace CSP.Models.HAL.Config;

public class MapModel
{
    public Dictionary<string, GroupModel> Groups { get; set; }

    [YamlIgnore]
    public ObservableDictionary<string, ObservableDictionary<string, Attribute>> Attributes { get; } = new();

    [YamlIgnore]
    public Dictionary<string, string> Total { get; } = new();

    public Dictionary<string, PropertyModel> Properties { get; set; }

    public static MapModel Load(string path) {
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(path), new ArgumentNullException(nameof(path)));

        if (!File.Exists(path)) {
            return null;
        }

        Deserializer deserializer = new();

        MapModel rtn;
        try {
            using (StreamReader reader = new(path)) {
                rtn = deserializer.Deserialize<MapModel>(reader);
            }
        }
        catch (InvalidOperationException e) {
            MessageBox.Show(e.Message, "error", MessageBoxButton.OK, MessageBoxImage.Error);

            return null;
        }

        DebugUtil.Assert(rtn != null, new ArgumentNullException("Map.YAML"), "YAML deserialization failed");

        foreach (var (_, group) in rtn!.Groups) {
            foreach (var (name, value) in group.Values) {
                rtn.Total.Add(name, value.Comment["zh-cn"]);
            }
        }

        foreach (var (propertyName, property) in rtn!.Properties) {
            ObservableDictionary<string, Attribute> attributes = new() {
                { "DisplayName", new DisplayNameAttribute(property.DisplayName["zh-cn"]) },
                { "Description", new DescriptionAttribute(property.Description["zh-cn"]) },
                { "Category", new CategoryAttribute(property.Category) },
                { "ReadOnly", new ReadOnlyAttribute(property.ReadOnly) }
            };
            rtn.Attributes.Add(propertyName, attributes);
        }

        return rtn;
    }

    public class GroupModel
    {
        public Dictionary<string, string> Comment { get; set; }

        public Dictionary<string, ValueModel> Values { get; set; }

        public class ValueModel
        {
            public Dictionary<string, string> Comment { get; set; }
        }
    }

    public class PropertyModel
    {
        public Dictionary<string, string> DisplayName { get; set; }

        public Dictionary<string, string> Description { get; set; }

        public string Category { get; set; }

        public bool ReadOnly { get; set; }
    }
}