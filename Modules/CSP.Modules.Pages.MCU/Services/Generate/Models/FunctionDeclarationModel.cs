using System.Collections.Generic;
using CSP.Utils.Extensions;

namespace CSP.Modules.Pages.MCU.Services.Generate.Models
{
    public class FunctionDeclarationModel
    {
        public string Name { get; set; }

        public List<ParameterModel> Parameters { get; } = new();

        public string Type { get; set; }

        public override string ToString()
        {
            var parameter = "";

            var count = Parameters.Count;
            for (var i = 0; i < count; i++)
            {
                if (count == 1)
                {
                    if (Parameters[0].Name.IsNullOrEmpty())
                    {
                        parameter += $"{Parameters[0].Type}";
                    }
                    else
                    {
                        parameter += $"{Parameters[0].Type} {Parameters[0].Name}";
                    }
                }
                else
                {
                    if (i == count - 1)
                    {
                        parameter += $"{Parameters[i].Type} {Parameters[i].Name}";
                    }
                    else
                    {
                        parameter += $"{Parameters[i].Type} {Parameters[i].Name}, ";
                    }
                }
            }

            var rtn = $"{Type} {Name}({parameter});";

            return rtn;
        }

        public class ParameterModel
        {
            public string Name { get; set; }
            public string Type { get; set; }
        }
    }
}