using CSP.Database.Models.MDK;

namespace CSP.Database
{
    public static class MDKHelper
    {
        private static readonly MDKInstance Instance = MDKInstance.Instance;

        private static UvprojxModel Uvprojx { get => Instance.Uvprojx; }

        public static UvprojxModel Load(string path) => Instance.Load(path);
    }
}