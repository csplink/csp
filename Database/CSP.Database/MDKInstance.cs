using CSP.Database.Models.MDK;
using System;

namespace CSP.Database
{
    internal class MDKInstance
    {
        private static readonly Lazy<MDKInstance> Lazy = new(static () => new MDKInstance());

        public UvprojxModel Uvprojx;

        private MDKInstance()
        {
        }

        public static MDKInstance Instance => Lazy.Value;

        public UvprojxModel Load(string path)
        {
            Uvprojx = UvprojxModel.Load(path);
            return Uvprojx;
        }
    }
}