using System;
using CSP.Models.DB;

namespace CSP.Singleton.DB;

internal class PackageSingletonInstance
{
    private static readonly Lazy<PackageSingletonInstance> Lazy = new(static () => new PackageSingletonInstance());

    private PackageSingletonInstance() {
    }

    public static PackageSingletonInstance Instance => Lazy.Value;

    public PackageModel Package { get; set; }
}