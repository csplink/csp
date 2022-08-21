namespace CSP.Modules.Pages.MCU.Services.Generate
{
    public class IncBase : GenerateBase
    {
        protected IncBase(string path = null) : base(path)
        {
        }

        public string Generate()
        {
            var content = "";

            content += RegionCopyright;
            content += Copyright;
            content += EndregionCopyright;
            content += "\n\n";

            content += Resources.Files.HeaderStart.Replace("${file}", $"CSP_{File}".ToUpper().Replace(".", "_") + "__");
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
            content += EndregionFunctionDeclarations;
            content += "\n\n";

            #endregion function_declarations

            content += Resources.Files.HeaderEnd;
            content += "\n";

            return content;
        }
    }
}