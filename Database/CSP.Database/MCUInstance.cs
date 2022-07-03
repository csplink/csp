using CSP.Database.Models.MCU;
using CSP.Resources;
using CSP.Utils.Extensions;
using Serilog;
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
            LoadMaps();
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
            if (company.IsNullOrEmpty())
                Log.Error(new ArgumentNullException(nameof(company)), "\"Company\" 参数为 NULL");
            if (name.IsNullOrEmpty())
                Log.Error(new ArgumentNullException(nameof(name)), "\"Name\" 参数为 NULL");

            Company = company;
            Name = name;

            var path = $"{IniFile.PathMCUDb}/Company/{company}/MCU/{name}.xml";
            MCU = MCUModel.Load(path);
            if (MCU == null)
            {
                Log.Error(new ArgumentNullException(nameof(MCU)), $"MCU \"{name}\" 读取失败");
            }

            LoadIP();
        }

        private void LoadIP()
        {
            var path = $"{IniFile.PathMCUDb}/Company/{Company}/IP/{Name}-IP.xml";
            IP = IPModel.Load(path);

            if (IP == null)
            {
                Log.Error(new ArgumentNullException(nameof(IP)), $"IP \"{Name}\" 读取失败");
            }
        }

        private void LoadMaps()
        {
            foreach (var name in MapNames)
            {
                _maps.Add(name, MapModel.Load($"{IniFile.PathMCUDb}/Map/{name}.xml"));
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