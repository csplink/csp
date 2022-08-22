using System;

namespace CSP.Services
{
    internal class ProjectInstance
    {
        private static readonly Lazy<ProjectInstance> Lazy = new(static () => new ProjectInstance());

        private ProjectInstance() {
        }

        public static ProjectInstance Instance => Lazy.Value;
    }
}