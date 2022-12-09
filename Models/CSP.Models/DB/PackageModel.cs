using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Windows;
using CSP.Utils;
using Json.Net;

namespace CSP.Models.DB;

public class PackageModel
{
    public AuthorModel Author { get; set; }

    public string Category { get; set; }

    public Dictionary<string, string> Description { get; set; }

    public string Homepage { get; set; }

    public string[] Keywords { get; set; }

    public string License { get; set; }

    public string Name { get; set; }

    public string Option { get; set; }

    public string Readme { get; set; }

    public string Repository { get; set; }

    public string Rule { get; set; }

    public string Target { get; set; }

    public string[] Versions { get; set; }

    public static PackageModel Load(string path) {
        DebugUtil.Assert(!string.IsNullOrWhiteSpace(path), new ArgumentNullException(nameof(path)));

        if (!File.Exists(path)) {
            return null;
        }

        PackageModel rtn;
        try {
            using (StreamReader reader = new(path)) {
                rtn = JsonNet.Deserialize<PackageModel>(reader, PropertyNameTransforms.TitleToCamelCase);
            }
        }
        catch (InvalidOperationException e) {
            MessageBox.Show(e.Message, "error", MessageBoxButton.OK, MessageBoxImage.Error);

            return null;
        }

        DebugUtil.Assert(rtn != null, new ArgumentNullException("Package.JSON"), "JSON deserialization failed");
        List<string> descriptionNames = new(rtn!.Description.Keys);
        foreach (string descriptionName in descriptionNames) {
            rtn.Description.Add(CultureInfo.CurrentCulture.TextInfo.ToTitleCase(descriptionName),
                rtn!.Description[descriptionName]);
            rtn.Description.Remove(descriptionName);
        }

        if (!rtn.Versions.Contains("latest")) {
            List<string> list = rtn!.Versions.ToList();
            list.Add("latest");
            rtn.Versions = list.ToArray();
        }

        return rtn;
    }

    public class AuthorModel
    {
        public string Email { get; set; }

        public string Github { get; set; }

        public string Name { get; set; }
    }
}