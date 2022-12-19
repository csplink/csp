using System;
using CSP.Models.DB.Chip;

namespace CSP.Singleton.DB.Chip;

internal class SummarySingletonInstance
{
    private static readonly Lazy<SummarySingletonInstance> Lazy = new(static () => new SummarySingletonInstance());

    private SummarySingletonInstance() {
    }

    public static SummarySingletonInstance Instance => Lazy.Value;

    public SummaryModel Summary { get; set; }
}