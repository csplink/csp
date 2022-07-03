using CSP.Services.Models;
using Serilog;
using System;

namespace CSP.Services
{
    public static class ProjectHelper
    {
        private static readonly ProjectInstance Instance = ProjectInstance.Instance;
        public static string Name { get; set; }
        public static string Path { get; set; }
        public static ProjectModel Project { get; set; }

        public static void Create(string path, ProjectModel model)
        {
            if (path == null)
                Log.Error(new ArgumentNullException(nameof(path)), "Path NULL");

            Path = path;
            Name = System.IO.Path.GetFileNameWithoutExtension(path);
            ProjectModel.Create(path, model);
            Project = model;
        }

        public static void Create(string path)
        {
            Create(path, Project);
        }

        public static ProjectModel Load(string path)
        {
            if (path == null)
                Log.Error(new ArgumentNullException(nameof(path)), "Path NULL");

            Path = path;
            Name = System.IO.Path.GetFileNameWithoutExtension(path);
            Project = ProjectModel.Load(path);
            return Project;
        }
    }
}