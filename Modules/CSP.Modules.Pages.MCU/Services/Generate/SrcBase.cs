using CSP.Modules.Pages.MCU.Services.Generate.Models;
using System.Collections.Generic;

namespace CSP.Modules.Pages.MCU.Services.Generate
{
    public class SrcBase : GenerateBase
    {
        protected SrcBase(string path = null) : base(path)
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
                        ReadUserInit(fileData);
                    }
                }
            }
        }

        #region region

        #region functions

        internal const string EndregionFunctions = "\n// endregion functions";
        internal const string EndregionUserFunctions = "\n// endregion user functions";
        internal const string RegionFunctions = "// region functions\n";
        internal const string RegionUserFunctions = "// region user functions\n";

        #endregion functions

        #region variables

        internal const string EndregionUserVariables = "\n// endregion user variables";
        internal const string EndregionVariables = "\n// endregion variables";
        internal const string RegionUserVariables = "// region user variables\n";
        internal const string RegionVariables = "// region variables\n";

        #endregion variables

        #region init

        internal const string EndregionUserInit = "\n// endregion user init";
        internal const string EndregionInit = "\n// endregion init";
        internal const string RegionUserInit = "// region user init\n";
        internal const string RegionInit = "// region init\n";

        #endregion init

        #endregion region

        internal List<FunctionModel> Functions { get; } = new();
        internal string UserFunctions { get; set; }
        internal string UserVariables { get; set; }
        internal string UserInit { get; set; }
        internal List<VariableModel> Variables { get; } = new();
        internal List<string> Init { get; } = new();

        public void AddFunction(FunctionModel function)
        {
            Functions.Add(function);
        }

        public void AddVariable(VariableModel variable)
        {
            Variables.Add(variable);
        }

        public void AddInit(string init)
        {
            Init.Add(init);
        }

        public string Generate()
        {
            var content = "";

            content += RegionCopyright;
            content += Copyright;
            content += EndregionCopyright;
            content += "\n\n";

            #region includes

            content += RegionIncludes;
            content += GenerateIncludes();
            content += EndregionIncludes;
            content += "\n\n";

            content += RegionUserIncludes;
            content += UserIncludes;
            content += EndregionUserIncludes;
            content += "\n\n";

            #endregion includes

            #region macros

            content += RegionMacros;
            content += GenerateMacros();
            content += EndregionMacros;
            content += "\n\n";

            content += RegionUserMacros;
            content += UserMacros;
            content += EndregionUserMacros;
            content += "\n\n";

            #endregion macros

            #region externs

            content += RegionExterns;
            content += GenerateExterns();
            content += EndregionExterns;
            content += "\n\n";

            content += RegionUserExterns;
            content += UserExterns;
            content += EndregionUserExterns;
            content += "\n\n";

            #endregion externs

            #region function_declarations

            content += RegionFunctionDeclarations;
            content += GenerateFunctionDeclarations();
            content += EndregionFunctionDeclarations;
            content += "\n\n";

            content += RegionUserFunctionDeclarations;
            content += UserFunctionDeclarations;
            content += EndregionUserFunctionDeclarations;
            content += "\n\n";

            #endregion function_declarations

            #region variables

            content += RegionVariables;
            content += GenerateVariables();
            content += EndregionVariables;
            content += "\n\n";

            content += RegionUserVariables;
            content += UserVariables;
            content += EndregionUserVariables;
            content += "\n\n";

            #endregion variables

            #region functions

            content += RegionFunctions;
            content += GenerateFunctions();
            content += EndregionFunctions;
            content += "\n\n";

            content += RegionUserFunctions;
            content += UserFunctions;
            content += EndregionUserFunctions;
            content += "\n\n";

            #endregion functions

            #region init

            content += RegionInit;
            content += GenerateInit();
            content += EndregionInit;
            content += "\n\n";

            content += RegionUserInit;
            content += UserInit;
            content += EndregionUserInit;
            content += "\n\n";

            #endregion init

            return content;
        }

        public string GenerateFunctions()
        {
            if (Functions.Count == 0)
                return "";

            var rtn = "\n";

            // ReSharper disable once ForeachCanBeConvertedToQueryUsingAnotherGetEnumerator
            foreach (var function in Functions)
            {
                rtn += function + "\n";
            }

            return rtn;
        }

        public string GenerateVariables()
        {
            if (Variables.Count == 0)
                return "";

            var rtn = "\n";

            // ReSharper disable once ForeachCanBeConvertedToQueryUsingAnotherGetEnumerator
            foreach (var variable in Variables)
            {
                rtn += variable + "\n";
            }

            return rtn;
        }

        public string GenerateInit()
        {
            if (Init.Count == 0)
                return "";

            var rtn = "\n";

            // ReSharper disable once ForeachCanBeConvertedToQueryUsingAnotherGetEnumerator
            foreach (var init in Init)
            {
                rtn += $"INIT_BOARD_EXPORT({init}());\n";
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

        public void RemoveInit(string init)
        {
            Init.Remove(init);
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

        private void ReadUserInit(string data)
        {
            UserInit = ReadUser(data, RegionUserInit, EndregionUserInit);
        }
    }
}