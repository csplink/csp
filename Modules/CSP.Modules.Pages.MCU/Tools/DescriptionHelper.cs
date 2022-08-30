using CSP.Models;
using CSP.Modules.Pages.MCU.Models;

namespace CSP.Modules.Pages.MCU.Tools
{
    public static class DescriptionHelper
    {
        private static readonly DescriptionInstance Instance = DescriptionInstance.Instance;
        public static MCUModel MCU { get => Instance.MCU; }
        public static PinoutModel Pinout { get => Instance.Pinout; }
    }
}