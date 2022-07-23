using CSP.Modules.Pages.MCU.Services.Generate.Models;
using CSP.Utils.Extensions;
using System;
using System.Collections.Generic;

namespace CSP.Modules.Pages.MCU.Services.Generate
{
    public class GenerateBase
    {
        internal readonly bool IsSys;

        protected GenerateBase(string path = null)
        {
            string fileData = null;

            if (path == null)
            {
                IsSys = true;
            }
            else
            {
                if (!System.IO.File.Exists(path))
                {
                    IsSys = true;
                }
                else
                {
                    fileData = System.IO.File.ReadAllText(path);
                    IsSys = false;
                }
            }

            if (IsSys)
            {
                Copyright = Resources.Files.Copyright;
                UpdateCopyright();
            }
            else
            {
                ReadCopyright(fileData);
                ReadUserIncludes(fileData);
                ReadUserMacros(fileData);
                ReadUserFunctionDeclarations(fileData);
            }
        }

        #region file

        private string _file;

        internal string File
        {
            get => _file;
            set
            {
                _file = value;
                if (IsSys)
                {
                    if (!File.IsNullOrEmpty())
                        Copyright = Copyright.Replace("${file}", File);
                }
            }
        }

        #endregion file

        #region brief

        private string _brief;

        internal string Brief
        {
            get => _brief;
            set
            {
                _brief = value;
                if (IsSys)
                {
                    if (!Brief.IsNullOrEmpty())
                        Copyright = Copyright.Replace("${brief}", Brief);
                }
            }
        }

        #endregion brief

        internal string Copyright { get; set; }
        internal List<ExternModel> Externs { get; } = new();
        internal List<FunctionDeclarationModel> FunctionDeclarations { get; } = new();
        internal List<IncModel> Includes { get; } = new();
        internal List<MacroModel> Macros { get; } = new();
        internal string UserExterns { get; set; }
        internal string UserFunctionDeclarations { get; set; }
        internal string UserIncludes { get; set; }
        internal string UserMacros { get; set; }
        internal string UserTypes { get; set; }

        #region region

        #region copyright

        internal const string EndregionCopyright = "\r\n// endregion copyright";
        internal const string RegionCopyright = "// region copyright\r\n";

        #endregion copyright

        #region includes

        internal const string EndregionIncludes = "\r\n// endregion includes";
        internal const string EndregionUserIncludes = "\r\n// endregion user includes";
        internal const string RegionIncludes = "// region includes\r\n";
        internal const string RegionUserIncludes = "// region user includes\r\n";

        #endregion includes

        #region types

        internal const string EndregionTypes = "\r\n// endregion types";
        internal const string EndregionUserTypes = "\r\n// endregion user types";
        internal const string RegionTypes = "// region types\r\n";
        internal const string RegionUserTypes = "// region user types\r\n";

        #endregion types

        #region macros

        internal const string EndregionMacros = "\r\n// endregion macros";
        internal const string EndregionUserMacros = "\r\n// endregion user macros";
        internal const string RegionMacros = "// region macros\r\n";
        internal const string RegionUserMacros = "// region user macros\r\n";

        #endregion macros

        #region externs

        internal const string EndregionExterns = "\r\n// endregion externs";
        internal const string EndregionUserExterns = "\r\n// endregion user externs";
        internal const string RegionExterns = "// region externs\r\n";
        internal const string RegionUserExterns = "// region user externs\r\n";

        #endregion externs

        #region function_declarations

        internal const string EndregionFunctionDeclarations = "\r\n// endregion function declarations";
        internal const string EndregionUserFunctionDeclarations = "\r\n// endregion user function declarations";
        internal const string RegionFunctionDeclarations = "// region function declarations\r\n";
        internal const string RegionUserFunctionDeclarations = "// region user function declarations\r\n";

        #endregion function_declarations

        #endregion region

        public void AddExtern(ExternModel ext)
        {
            Externs.Add(ext);
        }

        protected void AddFunctionDeclaration(FunctionDeclarationModel function)
        {
            FunctionDeclarations.Add(function);
        }

        protected void AddInclude(IncModel inc)
        {
            Includes.Add(inc);
        }

        protected void AddMacro(MacroModel macro)
        {
            Macros.Add(macro);
        }

        protected string GenerateExterns()
        {
            if (Externs.Count == 0)
                return "";

            var rtn = "\r\n";

            // ReSharper disable once ForeachCanBeConvertedToQueryUsingAnotherGetEnumerator
            foreach (var ext in Externs)
            {
                rtn += ext + "\r\n";
            }

            return rtn;
        }

        protected string GenerateFunctionDeclarations()
        {
            if (FunctionDeclarations.Count == 0)
                return "";

            var rtn = "\r\n";

            // ReSharper disable once ForeachCanBeConvertedToQueryUsingAnotherGetEnumerator
            foreach (var functionDeclaration in FunctionDeclarations)
            {
                rtn += functionDeclaration + "\r\n";
            }

            return rtn;
        }

        protected string GenerateIncludes()
        {
            if (Includes.Count == 0)
                return "";

            var rtn = "\r\n";

            // ReSharper disable once ForeachCanBeConvertedToQueryUsingAnotherGetEnumerator
            foreach (var include in Includes)
            {
                rtn += include + "\r\n";
            }

            return rtn;
        }

        protected string GenerateMacros()
        {
            if (Macros.Count == 0)
                return "";

            var rtn = "\r\n";

            // ReSharper disable once ForeachCanBeConvertedToQueryUsingAnotherGetEnumerator
            foreach (var macro in Macros)
            {
                rtn += macro + "\r\n";
            }

            return rtn;
        }

        public void RemoveExtern(ExternModel ext)
        {
            Externs.Remove(ext);
        }

        public void RemoveFunctionDeclaration(FunctionDeclarationModel function)
        {
            FunctionDeclarations.Remove(function);
        }

        public void RemoveInclude(IncModel inc)
        {
            Includes.Remove(inc);
        }

        public void RemoveMacro(MacroModel macro)
        {
            Macros.Remove(macro);
        }

        internal static string ReadUser(string value, string region, string endregion)
        {
            if (value.IsNullOrEmpty())
                throw new ArgumentNullException(nameof(value));
            if (region.IsNullOrEmpty())
                throw new ArgumentNullException(nameof(region));
            if (endregion.IsNullOrEmpty())
                throw new ArgumentNullException(nameof(endregion));

            if (value.Contains(region) && value.Contains(endregion))
            {
                var begin = value.IndexOf(region, StringComparison.Ordinal) + region.Length;
                var end = value.IndexOf(endregion, StringComparison.Ordinal);

                return value.Substring(begin, end - begin);
            }

            return "";
        }

        private void ReadCopyright(string data)
        {
            Copyright = ReadUser(data, RegionCopyright, EndregionCopyright);
        }

        private void ReadUserFunctionDeclarations(string data)
        {
            UserFunctionDeclarations = ReadUser(data, RegionUserFunctionDeclarations, EndregionUserFunctionDeclarations);
        }

        private void ReadUserIncludes(string data)
        {
            UserIncludes = ReadUser(data, RegionUserIncludes, EndregionUserIncludes);
        }

        private void ReadUserMacros(string data)
        {
            UserMacros = ReadUser(data, RegionUserMacros, EndregionUserMacros);
        }

        private void UpdateCopyright()
        {
            Copyright = Copyright.Replace("${author}               ", Environment.UserName.PadRight(18, ' '));
            Copyright = Copyright.Replace("${author}", Environment.UserName);
            var date = DateTime.Now;
            Copyright = Copyright.Replace("${year}", date.Year.ToString());
            Copyright = Copyright.Replace("${month}", date.Month.ToString().PadLeft(2, '0'));
            Copyright = Copyright.Replace("${day}", date.Day.ToString().PadLeft(2, '0'));
            Copyright = Copyright.Replace("${hour}", date.Hour.ToString().PadLeft(2, '0'));
            Copyright = Copyright.Replace("${minute}", date.Minute.ToString().PadLeft(2, '0'));
            Copyright = Copyright.Replace("${second}", date.Second.ToString().PadLeft(2, '0'));
        }
    }
}