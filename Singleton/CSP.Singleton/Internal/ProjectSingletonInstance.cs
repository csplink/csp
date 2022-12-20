using System;
using CSP.Models.Internal;

namespace CSP.Singleton.Internal;

internal class ProjectSingletonInstance
{
    private static readonly Lazy<ProjectSingletonInstance> Lazy = new(static () => new ProjectSingletonInstance());

    private ProjectSingletonInstance() {
    }

    public static ProjectSingletonInstance Instance => Lazy.Value;

    public ProjectModel Project { get; } = new();
}