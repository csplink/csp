namespace CSP.Modules.Pages.MCU.Services.Generate.Models
{
    public class MacroModel
    {
        public string Name { get; set; }

        public string Value { get; set; }

        public override string ToString()
        {
            return $"#define {Name} {Value}";
        }
    }
}