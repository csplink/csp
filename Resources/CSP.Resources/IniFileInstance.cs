using System;
using System.Collections.Generic;
using System.IO;
using System.Windows;
using CSP.Utils;
using YamlDotNet.Core;
using YamlDotNet.Serialization;

namespace CSP.Resources;

using config_t = Dictionary<string, Dictionary<string, string>>;

public class IniFileInstance
{
    private const    string                                         IniPath      = "./CSP.yaml";
    private readonly Dictionary<string, Dictionary<string, string>> _ini         = new();
    private readonly Deserializer                                   deserializer = new();
    private readonly Serializer                                     serializer   = new();

    public IniFileInstance() {
        if (!File.Exists(IniPath)) {
            InitData();
        }
        else {
            try {
                using (StreamReader reader = new(IniPath)) {
                    _ini = deserializer.Deserialize<config_t>(reader);
                }
            }
            catch (YamlException e) {
                MessageBox.Show(e.Message, "error", MessageBoxButton.OK, MessageBoxImage.Error);
            }

            DebugUtil.Assert(_ini != null, new ArgumentNullException("Repository.YAML"), "YAML deserialization failed");
        }
    }

    public void Save() {
        string str = serializer.Serialize(_ini);
        using (StreamWriter writer = new(IniPath)) {
            serializer.Serialize(writer, _ini);
        }
    }

    internal void AddKey(string section, string key, string value) {
        if (!_ini.ContainsKey(section)) {
            _ini[section] = new Dictionary<string, string>();
        }

        if (_ini[section].ContainsKey(key)) {
            _ini[section][key] = value;
        }
        else {
            _ini[section].Add(key, value);
        }
    }

    internal string ReadKey(string section, string key, string defaultValue) {
        if (!_ini.ContainsKey(section)) {
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
        AddKey("Path", "Repo", Path.Repo);
        Save();
    }
}