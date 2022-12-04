using IniParser;
using IniParser.Model;
using System.IO;

namespace CSP.Resources
{
    public class IniFileInstance
    {
        private const string IniPath = "./CSP.ini";
        private readonly IniData _ini = new();
        private readonly FileIniDataParser _parser = new();

        public IniFileInstance() {
            if (!File.Exists(IniPath)) {
                InitData();
            }
            else {
                _ini = _parser.ReadFile(IniPath);
            }
        }

        public void Save() {
            _parser.WriteFile(IniPath, _ini);
        }

        internal void AddKey(string section, string key, string value) {
            if (!_ini.Sections.ContainsSection(section)) {
                _ini.Sections.AddSection(section);
            }

            if (_ini[section].ContainsKey(key)) {
                _ini[section][key] = value;
            }
            else {
                _ini[section].AddKey(key, value);
            }
        }

        internal string ReadKey(string section, string key, string defaultValue) {
            if (!_ini.Sections.ContainsSection(section)) {
                AddKey(section, key, defaultValue);
                return defaultValue;
            }

            if (!_ini[section].ContainsKey(key)) {
                AddKey(section, key, defaultValue);
                return defaultValue;
            }

            return _ini[section][key];
        }

        private void InitData() {
            AddKey("Path", "Git", Path.Git);
            AddKey("Path", "LogFile", Path.LogFile);
            AddKey("Path", "MCUDb", Path.MCUDb);
            AddKey("Path", "MCUDbUrl", Path.MCUDbUrl);
            AddKey("Path", "Repo", Path.Repo);
            Save();
        }
    }
}
