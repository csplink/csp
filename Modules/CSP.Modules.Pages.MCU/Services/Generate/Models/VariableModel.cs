namespace CSP.Modules.Pages.MCU.Services.Generate.Models
{
    public class VariableModel
    {
        public bool IsStatic { get; set; }
        public string Name { get; set; }
        public string Type { get; set; }
        public string Value { get; set; }

        public override string ToString() {
            var sta = IsStatic ? "static " : "";
            var rtn = $"{sta}{Type} {Name} = {Value};";
            return rtn;
        }
    }
}