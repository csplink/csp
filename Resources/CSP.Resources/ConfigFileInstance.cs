// Licensed under the Apache License, Version 2.0 (the "License");
// You may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// Copyright (C) 2022-2023 xqyjlj<xqyjlj@126.com>
//
// @author      xqyjlj
// @file        ConfigFileInstance.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

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