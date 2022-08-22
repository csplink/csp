using CSP.Services.Models;
using CSP.Utils;
using System;

namespace CSP.Services
{
    public static class ProjectHelper
    {
        private static readonly ProjectInstance Instance = ProjectInstance.Instance;
        public static string Name { get; set; }
        public static string Path { get; set; }
        public static ProjectModel Project { get; set; }

        public static void Create(string path, ProjectModel model) {
            DebugUtil.Assert(path != null, new ArgumentNullException(nameof(path)));
            DebugUtil.Assert(model != null, new ArgumentNullException(nameof(model)));

            Path = path;
            Name = System.IO.Path.GetFileNameWithoutExtension(path);
            ProjectModel.Create(path, model);
            Project = model;
        }

        public static void Create(string path) {
            Create(path, Project);
        }

        public static ProjectModel Load(string path) {
            DebugUtil.Assert(path != null, new ArgumentNullException(nameof(path)));

            Path = path;
            Name = System.IO.Path.GetFileNameWithoutExtension(path);
            Project = ProjectModel.Load(path);
            return Project;
        }
    }
}