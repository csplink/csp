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

        if (oldKey != null) {
            oldKey = "CSP_USING_" + oldKey.ToUpper();
        }
        else {
            oldKey = "";
        }

        if (newKey != null) {
            newKey = "CSP_USING_" + newKey.ToUpper();
        }
        else {
            newKey = "";
        }

        if (Project.Defines.ContainsKey(oldKey!)) {
            Project.Defines.Remove(oldKey);
        }

        if (Project.Defines.ContainsKey(newKey!)) {
            Project.Defines.Remove(newKey);
        }

        Project.Defines.Add(newKey, newValue);
    }

    public static bool IsDependence(IEnumerable<string> dependencies) {
        if (dependencies == null) {
            return true;
        }

        bool isDependence = true;
        foreach (string dependence in dependencies) {
            if (!Project.Defines.ContainsKey(dependence)) {
                isDependence = false;
            }
        }

        return isDependence;
    }
}