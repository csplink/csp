using CSP.Events;
using CSP.Utils;
using YamlDotNet.Serialization;

namespace CSP.Models.Internal;

public class ProjectModel
{
    [YamlIgnore]
    public ObservableDictionary<string, string> Defines { get; } = new();

    [YamlIgnore]
    public ObservableDictionary<string, PropertyDetails> Properties { get; } = new();
}