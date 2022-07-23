using CSP.Database.Models.MDK;

namespace CSP.Database
{
    public class MDKHelper
    {
        public static ProjectModel Load(string path) => ProjectModel.Load(path);
    }
}