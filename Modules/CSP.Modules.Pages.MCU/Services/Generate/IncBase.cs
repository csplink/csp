namespace CSP.Modules.Pages.MCU.Services.Generate
{
    public class IncBase : GenerateBase
    {
        public IncBase(string path = null) : base(path)
        {
        }

        public string Generate()
        {
            var content = "";

            content += RegionCopyright;
            content += Copyright;
            content += EndregionCopyright;
            content += "\r\n\r\n";

            content += CSP.Modules.Pages.MCU.Resources.Files.HeaderStart.Replace("${file}", File.ToUpper().Replace(".", "_") + "__");
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
            content += EndregionFunctionDeclarations;
            content += "\r\n\r\n";

            #endregion function_declarations

            content += CSP.Modules.Pages.MCU.Resources.Files.HeaderEnd;
            content += "\r\n";

            return content;
        }
    }
}