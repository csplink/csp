using CSP.Database.Models.MCU;
using CSP.Resources;
using CSP.Utils;
using CSP.Utils.Extensions;
using System;
using System.Collections.Generic;

namespace CSP.Database
{
    internal class MCUInstance
    {
        private static readonly Lazy<MCUInstance> Lazy = new(static () => new MCUInstance());
        private static readonly string[] MapNames = { "GPIO" };
        private readonly Dictionary<string, MapModel> _maps = new();
        private IPModel _ip;
        private MCUModel _mcu;

        private MCUInstance()
        {
            Repository = RepositoryModel.Load($"{IniFile.PathMCUDb}/Repository.xml");
        }

        public static MCUInstance Instance => Lazy.Value;
        public string Company { get; private set; }

        public IPModel IP
        {
            get => _ip;
            private set
            {
                _ip = value;
                UpdatePinFunctionMode();
            }
        }

        public MCUModel MCU
        {
            get => _mcu;
            private set
            {
                _mcu = value;
                UpdatePinFunctionMode();
            }
        }

        public string Name { get; private set; }
        public RepositoryModel Repository { get; }

        public MapModel GetMap(string name)
        {
            return _maps.ContainsKey(name) ? _maps[name] : null;
        }

        public void LoadMCU(string company, string name)
        {
            DebugUtil.Assert(!company.IsNullOrEmpty(), new ArgumentNullException(nameof(company)));
            DebugUtil.Assert(!name.IsNullOrEmpty(), new ArgumentNullException(nameof(name)));

            Company = company;
            Name = name;

            var path = $"{IniFile.PathMCUDb}/Company/{company}/MCU/{name}.xml";
            MCU = MCUModel.Load(path);

            DebugUtil.Assert(MCU != null, new ArgumentNullException(nameof(MCU)), $"MCU \"{name}\" 读取失败");

            LoadIP();
            LoadMaps();
        }

        private void LoadIP()
        {
            var path = $"{IniFile.PathMCUDb}/Company/{Company}/IP/{Name}-IP.xml";
            IP = IPModel.Load(path);

            DebugUtil.Assert(IP != null, new ArgumentNullException(nameof(IP)), $"MCU \"{Name}\" 读取失败");
        }

        private void LoadMaps()
        {
            _maps.Clear();
            foreach (var name in MapNames)
            {
                _maps.Add(name, MapModel.Load($"{IniFile.PathMCUDb}/Company/{Company}/Map/{MCU.Line}/{name}.xml"));
            }
        }

        private void UpdatePinFunctionMode()
        {
            if (MCU == null || IP == null)
                return;

            foreach (var pin in MCU.Pins)
            {
                if (pin.Functions != null)
                {
                    // ReSharper disable once ForeachCanBePartlyConvertedToQueryUsingAnotherGetEnumerator
                    foreach (var function in pin.Functions)
                    {
                        if (!function.Value.ModeName.IsNullOrEmpty() && IP.GPIO.Modes.ContainsKey(function.Value.ModeName))
                        {
                            function.Value.Mode = IP.GPIO.Modes[function.Value.ModeName];
                        }
                    }
                }
            }
        }
    }
}