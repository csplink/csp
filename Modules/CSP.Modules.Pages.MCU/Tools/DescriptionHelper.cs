using CSP.Components.ValuePropertyGrid;
using CSP.Events;
using CSP.Models;
using CSP.Modules.Pages.MCU.Models;
using CSP.Modules.Pages.MCU.Models.Description;
using CSP.Resources;
using CSP.Utils;
using CSP.Utils.Extensions;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;

namespace CSP.Modules.Pages.MCU.Tools
{
    public static class DescriptionHelper
    {
        private static readonly DescriptionInstance Instance = DescriptionInstance.Instance;

        public static ClockModel Clock { get => Instance.Clock; }

        public static string Company { get => Instance.Company; }

        public static ObservableDictionary<string, string> Defines { get => Instance.Defines; }

        public static MCUModel MCU { get => Instance.MCU; }

        public static string Name { get => Instance.Name; }

        public static PinoutModel Pinout { get => Instance.Pinout; }

        public static ObservableDictionary<string, PropertyDetails> Properties { get => Instance.Properties; }

        public static string RepositoryPath { get => Instance.RepositoryPath; }

        public static PropertyDetails CreateClockPropertyDetails() {
            var property = new PropertyDetails();
            var clockMap = GetMap("Clock");
            var clockIP = GetIP("Clock");
            foreach (var mode in clockIP.ModeMap) {
                foreach (var parameter in clockIP.ModeMap[mode.Key].ParameterMap) {
                    var map = new ObservableDictionary<string, string>();

                    foreach (var value in parameter.Value.Values) {
                        if (clockMap.Total.ContainsKey(value)) {
                            map.Add(value, clockMap.Total[value]);
                        }
                    }

                    var model = new DictionaryEditorModel {
                        Source = map
                    };
                    model.PropertyChanged += (sender, e) => {
                        if (sender is not DictionaryEditorModel)
                            return;

                        switch (e.PropertyName) {
                            case "Value": {
                                }

                                break;
                        }
                    };
                    property.Details.Add(parameter.Key, model);
                    property.Attributes.Add(parameter.Key, clockMap.Attributes[parameter.Key]);
                }
            }

            return property;
        }

        public static IPModel GetIP(string name) {
            return Instance.GetIP(name.ToUpper());
        }

        public static MapModel GetMap(string name) {
            return Instance.GetMap(name.ToUpper());
        }

        public static PinModel GetPinProperty(string name) {
            return Instance.GetPinProperty(name);
        }

        public static bool Load(MCUModel mcu) {
            DebugUtil.Assert(mcu != null, new ArgumentNullException(nameof(mcu)), "MCU不能为空");
            if (mcu == null)
                return false;

            Instance.MCU = mcu;

            return true;
        }

        public static bool Load(string company, string name) {
            DebugUtil.Assert(!company.IsNullOrEmpty(), new ArgumentNullException(nameof(company)), "company不能为空");
            DebugUtil.Assert(!name.IsNullOrEmpty(), new ArgumentNullException(nameof(name)), "name不能为空");
            if (company == null || name == null)
                return false;

            return Load(MCUModel.Load($"{IniFile.PathMCUDb}/{company}/{name}.xml"));
        }
    }
}