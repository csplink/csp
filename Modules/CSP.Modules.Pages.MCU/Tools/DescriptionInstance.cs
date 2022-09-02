using CSP.Models;
using CSP.Modules.Pages.MCU.Models;
using CSP.Resources;
using CSP.Utils;
using System;

namespace CSP.Modules.Pages.MCU.Tools
{
    internal class DescriptionInstance
    {
        private static readonly Lazy<DescriptionInstance> Lazy = new(static () => new DescriptionInstance());
        private MCUModel _mcu;

        private DescriptionInstance() {
        }

        public static DescriptionInstance Instance => Lazy.Value;
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

            return true;
        }
    }
}