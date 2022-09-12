using CSP.Components.ValuePropertyGrid;
using CSP.Events;
using CSP.Models;
using CSP.Modules.Pages.MCU.Models;
using CSP.Modules.Pages.MCU.Models.Repository;
using CSP.Resources;
using CSP.Utils;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;

namespace CSP.Modules.Pages.MCU.Tools
{
    internal class DescriptionInstance
    {
        private static readonly Lazy<DescriptionInstance> Lazy = new(static () => new DescriptionInstance());
        private MCUModel _mcu;

        private DescriptionInstance() {
        }

        public static DescriptionInstance Instance => Lazy.Value;
        private readonly Dictionary<string, MapModel> _maps = new();
        private readonly Dictionary<string, IPModel> _ips = new();
        private readonly Dictionary<string, PinModel> _pinProperties = new();
        public string Company { get; private set; }

        public MCUModel MCU {
            get => _mcu;
            set {
                _mcu = value;
                Load(value);
            }
        }

        public string Name { get; private set; }
        public PinoutModel Pinout { get; private set; }
        public string RepositoryPath { get; private set; }
        public ObservableCollection<KeyValuePair<string, string>> Defines { get; } = new();
        public ObservableDictionary<string, PropertyDetails> Properties { get; } = new();

        private bool Load(MCUModel mcu) {
            DebugUtil.Assert(mcu != null, new ArgumentNullException(nameof(mcu)), "MCU不能为空");
            if (mcu == null)
                return false;
#if DEBUG
            RepositoryPath = $"{IniFile.PathRepository}/{DescriptionHelper.MCU.HAL.Name.ToLower()}";
#else
            RepositoryPath =
                $"{IniFile.PathRepository}/{DescriptionHelper.MCU.HAL.Name.ToLower()}-{DescriptionHelper.MCU.HAL.Version.ToLower()}";
#endif
            Company = mcu.Company;
            Name = mcu.Name;

            Pinout = PinoutModel.Load($"{RepositoryPath}/description/{DescriptionHelper.MCU.Name.ToLower()}/pinout.xml");
            if (Pinout == null) return false;

            LoadMap($"{RepositoryPath}/description/map");
            LoadIP($"{RepositoryPath}/description/{DescriptionHelper.MCU.Name.ToLower()}/ip");

            foreach (var pin in Pinout.Pins) {
                if (!_pinProperties.ContainsKey(pin.Name))
                    _pinProperties.Add(pin.Name, new PinModel {
                        Name = new StringEditorModel { String = pin.Name },
                        Position = new StringEditorModel { String = pin.Position.ToString() }
                    });
                else {
                    MessageBoxUtil.Error($"存在相同的Pin：{pin.Name}");
                }
            }

            return true;
        }

        private bool LoadMap(string path) {
            DebugUtil.Assert(path != null, new ArgumentNullException(nameof(path)), "path不能为空");
            DebugUtil.Assert(Directory.Exists(path), new DirectoryNotFoundException(nameof(path)), $"{path} 不存在");

            if (path == null)
                return false;
            if (!Directory.Exists(path))
                return false;

            FileInfo[] files = new DirectoryInfo(path).GetFiles("*.xml", SearchOption.AllDirectories);
            foreach (var file in files) {
                var name = file.Name[..^".xml".Length].ToUpper();
                var model = MapModel.Load(file.FullName);
                if (!_maps.ContainsKey(file.Name))
                    _maps.Add(name, model);
                else
                    _maps[name] = model;
            }
            return true;
        }

        private bool LoadIP(string path) {
            DebugUtil.Assert(path != null, new ArgumentNullException(nameof(path)), "path不能为空");
            DebugUtil.Assert(Directory.Exists(path), new DirectoryNotFoundException(nameof(path)), $"{path} 不存在");

            if (path == null)
                return false;
            if (!Directory.Exists(path))
                return false;

            FileInfo[] files = new DirectoryInfo(path).GetFiles("*.xml", SearchOption.AllDirectories);
            foreach (var file in files) {
                var name = file.Name[..^".xml".Length].ToUpper();
                var model = IPModel.Load(file.FullName);
                if (!_ips.ContainsKey(file.Name))
                    _ips.Add(name, model);
                else
                    _ips[name] = model;
            }
            return true;
        }

        public MapModel GetMap(string name) {
            return _maps.ContainsKey(name) ? _maps[name] : null;
        }

        public IPModel GetIP(string name) {
            return _ips.ContainsKey(name) ? _ips[name] : null;
        }

        public PinModel GetPinProperty(string name) {
            return _pinProperties.ContainsKey(name) ? _pinProperties[name] : null;
        }
    }
}