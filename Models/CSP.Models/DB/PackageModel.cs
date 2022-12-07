using CSP.Utils;
using Json.Net;
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Windows;

namespace CSP.Models.DB
{
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
            DebugUtil.Assert(!string.IsNullOrEmpty(path), new ArgumentNullException(nameof(path)));

            if (!File.Exists(path))
                return null;

            PackageModel rtn;
            try {
                using (var reader = new StreamReader(path)) {
                    rtn = JsonNet.Deserialize<PackageModel>(reader, PropertyNameTransforms.TitleToCamelCase);
                }
            }
            catch (InvalidOperationException e) {
                MessageBox.Show(e.Message, "error", MessageBoxButton.OK, MessageBoxImage.Error);
                return null;
            }

            DebugUtil.Assert(rtn != null, new ArgumentNullException("Package.JSON"), "JSON deserialization failed");
            var descriptionNames = new List<string>(rtn!.Description.Keys);
            foreach (var descriptionName in descriptionNames) {
                rtn.Description.Add(CultureInfo.CurrentCulture.TextInfo.ToTitleCase(descriptionName), rtn!.Description[descriptionName]);
                rtn.Description.Remove(descriptionName);
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
}