import os

template_ini_file_data = """
        public static string {section}{name} {{
            get => Ini.ReadKey("{section}", "{name}", {section}.{name});
            set => Ini.AddKey("{section}", "{name}", value);
        }}
"""

template_ini_file = """namespace CSP.Resources
{{
    public static class IniFile
    {{
        private static readonly IniFileInstance Ini = new();
{data}
        public static void Save() {{
            Ini.Save();
        }}
    }}
}}
"""

template_ini_file_instance_data = """            AddKey("{section}", "{name}", {section}.{name});\n"""

template_ini_file_instance = """using IniParser;
using IniParser.Model;
using System.IO;

namespace CSP.Resources
{{
    public class IniFileInstance
    {{
        private const string IniPath = "./CSP.ini";
        private readonly IniData _ini = new();
        private readonly FileIniDataParser _parser = new();

        public IniFileInstance() {{
            if (!File.Exists(IniPath)) {{
                InitData();
            }}
            else {{
                _ini = _parser.ReadFile(IniPath);
            }}
        }}

        public void Save() {{
            _parser.WriteFile(IniPath, _ini);
        }}

        internal void AddKey(string section, string key, string value) {{
            if (!_ini.Sections.ContainsSection(section)) {{
                _ini.Sections.AddSection(section);
            }}

            if (_ini[section].ContainsKey(key)) {{
                _ini[section][key] = value;
            }}
            else {{
                _ini[section].AddKey(key, value);
            }}
        }}

        internal string ReadKey(string section, string key, string defaultValue) {{
            if (!_ini.Sections.ContainsSection(section)) {{
                AddKey(section, key, defaultValue);
                return defaultValue;
            }}

            if (!_ini[section].ContainsKey(key)) {{
                AddKey(section, key, defaultValue);
                return defaultValue;
            }}

            return _ini[section][key];
        }}

        private void InitData() {{
{data}            Save();
        }}
    }}
}}
"""

dir_resources = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "/Resources/CSP.Resources"
path_resources_ini_file = dir_resources + "/IniFile.cs"
path_resources_ini_file_instance = dir_resources + "/IniFileInstance.cs"
path_resources_path_designer = dir_resources + "/Path.Designer.cs"


def main():
    ini_file_data = ""
    ini_file_instance_data = ""
    with open(path_resources_path_designer, "r", encoding="utf-8") as fp:
        lines = fp.readlines()
        for line in lines:
            if line.startswith("        internal static string") and line.endswith(" {\n") and "::" not in line:
                name = line.replace("internal static string", "").replace(" {", "").strip()
                ini_file_data += template_ini_file_data.format(section="Path", name=name)
                ini_file_instance_data += template_ini_file_instance_data.format(section="Path", name=name)
    ini_file = template_ini_file.format(data=ini_file_data)
    ini_file_instance = template_ini_file_instance.format(data=ini_file_instance_data)

    with open(path_resources_ini_file, "w", encoding="utf-8") as fp:
        fp.write(ini_file)

    with open(path_resources_ini_file_instance, "w", encoding="utf-8") as fp:
        fp.write(ini_file_instance)


if __name__ == "__main__":
    main()
