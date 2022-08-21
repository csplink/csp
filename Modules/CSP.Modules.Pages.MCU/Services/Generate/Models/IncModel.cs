namespace CSP.Modules.Pages.MCU.Services.Generate.Models
{
    public class IncModel
    {
        public bool IsSys { get; set; }
        public string Name { get; set; }

        public override string ToString()
        {
            return IsSys ? $"#include <{Name}>" : $"#include \"{Name}\"";
        }
    }
}