using CSP.Models;
using CSP.Modules.Pages.MCU.Models;
using CSP.Resources;
using CSP.Utils;
using System;
using System.Collections.Generic;
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
        public string Company { get; set; }

        public MCUModel MCU {
            get => _mcu;
            set {
                _mcu = value;
                Load(value);
            }
        }

        public string Name { get; set; }
        public PinoutModel Pinout { get; set; }
        public string RepositoryPath { get; set; }

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

            LoadMap($"{RepositoryPath}/description/map");
            LoadIP($"{RepositoryPath}/description/{DescriptionHelper.MCU.Name.ToLower()}/ip");

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

        public MapModel GetMap(string name) {
            return _maps.ContainsKey(name) ? _maps[name] : null;
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

        public IPModel GetIP(string name) {
            return _ips.ContainsKey(name) ? _ips[name] : null;
        }
    }
}