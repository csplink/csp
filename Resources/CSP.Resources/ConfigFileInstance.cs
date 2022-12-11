using System;
using System.Collections.Generic;
using System.IO;
using System.Windows;
using CSP.Utils;
using YamlDotNet.Core;
using YamlDotNet.Serialization;

namespace CSP.Resources;

using config_t = Dictionary<string, Dictionary<string, string>>;

public class ConfigFileInstance
{
    private readonly config_t     _config       = new();
    private readonly string       _configPath   = "./CSP.yaml";
    private readonly Deserializer _deserializer = new();
    private readonly Serializer   _serializer   = new();

    public ConfigFileInstance() {
        if (!File.Exists(_configPath)) {
            InitData();
        }
        else {
            try {
                using (StreamReader reader = new(_configPath)) {
                    _config = _deserializer.Deserialize<config_t>(reader);
                }
            }
            catch (YamlException e) {
                MessageBox.Show(e.Message, "error", MessageBoxButton.OK, MessageBoxImage.Error);
            }

            DebugUtil.Assert(_config != null, new ArgumentNullException("ConfigFile.YAML"),
                "YAML deserialization failed");
        }
    }

    public void Save() {
        using (StreamWriter writer = new(_configPath)) {
            _serializer.Serialize(writer, _config);
        }
    }

    internal void AddKey(string section, string key, string value) {
        if (!_config.ContainsKey(section)) {
            _config[section] = new Dictionary<string, string>();
        }

        if (_config[section].ContainsKey(key)) {
            _config[section][key] = value;
        }
        else {
            _config[section].Add(key, value);
        }
    }

    internal string ReadKey(string section, string key, string defaultValue) {
        if (!_config.ContainsKey(section)) {
            AddKey(section, key, defaultValue);

            return defaultValue;
        }

        if (!_config[section].ContainsKey(key)) {
            AddKey(section, key, defaultValue);

            return defaultValue;
        }

        return _config[section][key];
    }

    private void InitData() {
        AddKey("Path", "Git", Path.Git);
        AddKey("Path", "LogFile", Path.LogFile);
        AddKey("Path", "Repo", Path.Repo);
        Save();
    }
}