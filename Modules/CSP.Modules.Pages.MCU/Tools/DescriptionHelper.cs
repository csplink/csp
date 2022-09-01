using System;
using CSP.Models;
using CSP.Modules.Pages.MCU.Models;
using CSP.Resources;
using CSP.Utils;
using CSP.Utils.Extensions;

namespace CSP.Modules.Pages.MCU.Tools
{
    public static class DescriptionHelper
    {
        private static readonly DescriptionInstance Instance = DescriptionInstance.Instance;
        public static string Company { get => Instance.Company; }
        public static MCUModel MCU { get => Instance.MCU; }
        public static string Name { get => Instance.Name; }
        public static PinoutModel Pinout { get => Instance.Pinout; }
        public static string RepositoryPath { get => Instance.RepositoryPath; }

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