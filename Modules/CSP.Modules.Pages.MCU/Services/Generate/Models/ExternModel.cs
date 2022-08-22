namespace CSP.Modules.Pages.MCU.Services.Generate.Models
{
    public class ExternModel
    {
        public string Name { get; set; }

        public string Type { get; set; }

        public override string ToString() {
            return $"extern {Type} {Name};";
        }
    }
}