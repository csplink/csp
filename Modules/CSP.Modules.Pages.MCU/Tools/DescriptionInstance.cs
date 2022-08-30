using CSP.Modules.Pages.MCU.Models;
using System;
using CSP.Models;

namespace CSP.Modules.Pages.MCU.Tools
{
    internal class DescriptionInstance
    {
        private static readonly Lazy<DescriptionInstance> Lazy = new(static () => new DescriptionInstance());

        private DescriptionInstance() {
        }

        public static DescriptionInstance Instance => Lazy.Value;

        public string Company { get; set; }
        public MCUModel MCU { get; set; }
        public string Name { get; set; }
        public PinoutModel Pinout { get; set; }
    }
}