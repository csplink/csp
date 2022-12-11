import os

template_config_file_data = """
    public static string {section}{name} {{
        get => Config.ReadKey("{section}", "{name}", {section}.{name});
        set => Config.AddKey("{section}", "{name}", value);
    }}
"""

template_config_file = """namespace CSP.Resources;

public static class ConfigFile
{{
    private static readonly ConfigFileInstance Config = new();
{data}
    public static void Save() {{
        Config.Save();
    }}
}}"""

template_config_file_instance_data = """        AddKey("{section}", "{name}", {section}.{name});\n"""

template_config_file_instance = """using System;
using System.Collections.Generic;
using System.IO;
using System.Windows;
using CSP.Utils;
using YamlDotNet.Core;
using YamlDotNet.Serialization;

namespace CSP.Resources;

using config_t = Dictionary<string, Dictionary<string, string>>;

public class ConfigFileInstance
{{
    private readonly config_t     _config       = new();
    private readonly string       _configPath   = "./CSP.yaml";
    private readonly Deserializer _deserializer = new();
    private readonly Serializer   _serializer   = new();

    public ConfigFileInstance() {{
        if (!File.Exists(_configPath)) {{
            InitData();
        }}
        else {{
            try {{
                using (StreamReader reader = new(_configPath)) {{
                    _config = _deserializer.Deserialize<config_t>(reader);
                }}
            }}
            catch (YamlException e) {{
                MessageBox.Show(e.Message, "error", MessageBoxButton.OK, MessageBoxImage.Error);
            }}

            DebugUtil.Assert(_config != null, new ArgumentNullException("ConfigFile.YAML"),
                "YAML deserialization failed");
        }}
    }}

    public void Save() {{
        using (StreamWriter writer = new(_configPath)) {{
            _serializer.Serialize(writer, _config);
        }}
    }}

    internal void AddKey(string section, string key, string value) {{
        if (!_config.ContainsKey(section)) {{
            _config[section] = new Dictionary<string, string>();
        }}

        if (_config[section].ContainsKey(key)) {{
            _config[section][key] = value;
        }}
        else {{
            _config[section].Add(key, value);
        }}
    }}

    internal string ReadKey(string section, string key, string defaultValue) {{
        if (!_config.ContainsKey(section)) {{
            AddKey(section, key, defaultValue);

            return defaultValue;
        }}

        if (!_config[section].ContainsKey(key)) {{
            AddKey(section, key, defaultValue);

            return defaultValue;
        }}

        return _config[section][key];
    }}

    private void InitData() {{
{data}        Save();
    }}
}}"""

dir_resources = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "/Resources/CSP.Resources"
path_resources_config_file = dir_resources + "/ConfigFile.cs"
path_resources_config_file_instance = dir_resources + "/ConfigFileInstance.cs"
path_resources_path_designer = dir_resources + "/Path.Designer.cs"


def main():
    config_file_data = ""
    config_file_instance_data = ""
    with open(path_resources_path_designer, "r", encoding="utf-8") as fp:
        lines = fp.readlines()
        for line in lines:
            if line.startswith("        internal static string") and line.endswith(" {\n") and "::" not in line:
                name = line.replace("internal static string", "").replace(" {", "").strip()
                config_file_data += template_config_file_data.format(section="Path", name=name)
                config_file_instance_data += template_config_file_instance_data.format(section="Path", name=name)
    config_file = template_config_file.format(data=config_file_data)
    config_file_instance = template_config_file_instance.format(data=config_file_instance_data)

    with open(path_resources_config_file, "w", encoding="utf-8") as fp:
        fp.write(config_file)

    with open(path_resources_config_file_instance, "w", encoding="utf-8") as fp:
        fp.write(config_file_instance)


if __name__ == "__main__":
    main()
