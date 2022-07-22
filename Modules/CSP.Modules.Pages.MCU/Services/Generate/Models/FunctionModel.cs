using CSP.Utils.Extensions;
using System.Collections.Generic;

namespace CSP.Modules.Pages.MCU.Services.Generate.Models
{
    public class FunctionModel
    {
        public List<FunctionUseModel> FunctionUses { get; } = new();

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

            var rtn = $"{Type} {Name}({parameter})\r\n";
            rtn += "{\r\n";

            foreach (var function in FunctionUses)
            {
                rtn += $"    {function}";
            }

            rtn += "}";
            return rtn;
        }

        public class FunctionUseModel
        {
            public string Name { get; set; }
            public List<string> Parameters { get; } = new();

            public override string ToString()
            {
                var parameter = "";

                if (Name.IsNullOrEmpty())
                    return "\r\n";

                var count = Parameters.Count;
                for (var i = 0; i < count; i++)
                {
                    if (count == 1)
                    {
                        parameter += $"{Parameters[0]}";
                    }
                    else
                    {
                        if (i == count - 1)
                        {
                            parameter += $"{Parameters[i]}";
                        }
                        else
                        {
                            parameter += $"{Parameters[i]}, ";
                        }
                    }
                }

                var rtn = $"{Name}({parameter});\r\n";
                return rtn;
            }
        }

        public class ParameterModel
        {
            public string Name { get; set; }
            public string Type { get; set; }
        }
    }
}