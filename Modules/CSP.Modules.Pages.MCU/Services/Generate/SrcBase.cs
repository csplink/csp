using CSP.Modules.Pages.MCU.Services.Generate.Models;
using System.Collections.Generic;

namespace CSP.Modules.Pages.MCU.Services.Generate
{
    public class SrcBase : GenerateBase
    {
        public SrcBase(string path = null) : base(path)
        {
            if (!IsSys)
            {
                if (path != null)
                {
                    if (System.IO.File.Exists(path))
                    {
                        var fileData = System.IO.File.ReadAllText(path);
                        ReadUserFunctions(fileData);
                        ReadUserVariables(fileData);
                        ReadUserExterns(fileData);
                    }
                }
            }
        }

        #region region

        #region functions

        internal const string EndregionFunctions = "\r\n// endregion functions";
        internal const string EndregionUserFunctions = "\r\n// endregion user functions";
        internal const string RegionFunctions = "// region functions\r\n";
        internal const string RegionUserFunctions = "// region user functions\r\n";

        #endregion functions

        #region variables

        internal const string EndregionUserVariables = "\r\n// endregion user variables";
        internal const string EndregionVariables = "\r\n// endregion variables";
        internal const string RegionUserVariables = "// region user variables\r\n";
        internal const string RegionVariables = "// region variables\r\n";

        #endregion variables

        #endregion region

        internal List<FunctionModel> Functions { get; } = new();
        internal string UserFunctions { get; set; }
        internal string UserVariables { get; set; }
        internal List<VariableModel> Variables { get; } = new();

        public void AddFunction(FunctionModel function)
        {
            Functions.Add(function);
        }

        public void AddVariable(VariableModel variable)
        {
            Variables.Add(variable);
        }

        public string Generate()
        {
            var content = "";

            content += RegionCopyright;
            content += Copyright;
            content += EndregionCopyright;
            content += "\r\n\r\n";

            #region includes

            content += RegionIncludes;
            content += GenerateIncludes();
            content += EndregionIncludes;
            content += "\r\n\r\n";

            content += RegionUserIncludes;
            content += UserIncludes;
            content += EndregionUserIncludes;
            content += "\r\n\r\n";

            #endregion includes

            #region macros

            content += RegionMacros;
            content += GenerateMacros();
            content += EndregionMacros;
            content += "\r\n\r\n";

            content += RegionUserMacros;
            content += UserMacros;
            content += EndregionUserMacros;
            content += "\r\n\r\n";

            #endregion macros

            #region externs

            content += RegionExterns;
            content += GenerateExterns();
            content += EndregionExterns;
            content += "\r\n\r\n";

            content += RegionUserExterns;
            content += UserExterns;
            content += EndregionUserExterns;
            content += "\r\n\r\n";

            #endregion externs

            #region function_declarations

            content += RegionFunctionDeclarations;
            content += GenerateFunctionDeclarations();
            content += EndregionFunctionDeclarations;
            content += "\r\n\r\n";

            content += RegionUserFunctionDeclarations;
            content += UserFunctionDeclarations;
            content += EndregionUserFunctionDeclarations;
            content += "\r\n\r\n";

            #endregion function_declarations

            #region variables

            content += RegionVariables;
            content += GenerateVariables();
            content += EndregionVariables;
            content += "\r\n\r\n";

            content += RegionUserVariables;
            content += UserVariables;
            content += EndregionUserVariables;
            content += "\r\n\r\n";

            #endregion variables

            #region functions

            content += RegionFunctions;
            content += GenerateFunctions();
            content += EndregionFunctions;
            content += "\r\n\r\n";

            content += RegionUserFunctions;
            content += UserFunctions;
            content += EndregionUserFunctions;
            content += "\r\n\r\n";

            #endregion functions

            return content;
        }

        public string GenerateFunctions()
        {
            if (Functions.Count == 0)
                return "";

            var rtn = "\r\n";

            // ReSharper disable once ForeachCanBeConvertedToQueryUsingAnotherGetEnumerator
            foreach (var function in Functions)
            {
                rtn += function + "\r\n";
            }

            return rtn;
        }

        public string GenerateVariables()
        {
            if (Variables.Count == 0)
                return "";

            var rtn = "\r\n";

            // ReSharper disable once ForeachCanBeConvertedToQueryUsingAnotherGetEnumerator
            foreach (var variable in Variables)
            {
                rtn += variable + "\r\n";
            }

            return rtn;
        }

        public void RemoveFunction(FunctionModel function)
        {
            Functions.Remove(function);
        }

        public void RemoveVariable(VariableModel variable)
        {
            Variables.Remove(variable);
        }

        private void ReadUserExterns(string data)
        {
            UserExterns = ReadUser(data, RegionUserExterns, EndregionUserExterns);
        }

        private void ReadUserFunctions(string data)
        {
            UserFunctions = ReadUser(data, RegionUserFunctions, EndregionUserFunctions);
        }

        private void ReadUserVariables(string data)
        {
            UserVariables = ReadUser(data, RegionUserVariables, EndregionUserVariables);
        }
    }
}