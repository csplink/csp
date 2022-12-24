using CSP.Models.DB;

namespace CSP.Singleton.DB;

public static class PackageSingleton
{
    private static readonly PackageSingletonInstance Instance = PackageSingletonInstance.Instance;

    public static PackageModel Package => Instance.Package;


    public static bool Set(string path) {
        Instance.Package = PackageModel.Load(path);

        return Instance.Package != null;
    }
}