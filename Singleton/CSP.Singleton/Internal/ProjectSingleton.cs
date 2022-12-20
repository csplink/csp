using System;
using System.Collections.Generic;
using CSP.Models.Internal;
using CSP.Utils;

namespace CSP.Singleton.Internal;

public static class ProjectSingleton
{
    private static readonly ProjectSingletonInstance Instance = ProjectSingletonInstance.Instance;

    public static ProjectModel Project => Instance.Project;

    public static void ChangeDefine(string oldKey, string newKey, string newValue) {
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(oldKey) || !string.IsNullOrWhiteSpace(newKey),
            new ArgumentNullException(nameof(oldKey) + " or " + nameof(newKey)), "oldKey 或者 newKey 不能均为空");
        if (Project.DefinesI.ContainsKey(oldKey!)) {
            Project.DefinesI.Remove(oldKey);
        }

        if (Project.DefinesI.ContainsKey(newKey!)) {
            Project.DefinesI.Remove(newKey);
        }

        Project.DefinesI.Add(newKey, newValue);
    }

    public static bool IsDependence(IEnumerable<string> dependencies) {
        if (dependencies == null) {
            return true;
        }

        bool isDependence = true;
        foreach (string dependence in dependencies) {
            if (!Project.DefinesI.ContainsKey(dependence)) {
                isDependence = false;
            }
        }

        return isDependence;
    }
}