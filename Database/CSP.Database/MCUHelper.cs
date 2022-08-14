using CSP.Database.Models.MCU;

namespace CSP.Database
{
    public static class MCUHelper
    {
        private static readonly MCUInstance Instance = MCUInstance.Instance;

        public static string Company { get => Instance.Company; }
        public static IPModel IP { get => Instance.IP; }
        public static MCUModel MCU { get => Instance.MCU; }
        public static string Name { get => Instance.Name; }
        public static RepositoryModel Repository { get => Instance.Repository; }

        public static MapModel GetMap(string name)
        {
            return Instance.GetMap(name);
        }

        public static void LoadMcu(string company, string name)
        {
            Instance.LoadMCU(company, name);
        }

        public static void GenerateMap(string source, string dest)
        {
            var model = MapModel.Transform(source);
            MapModel.Create(dest, model);
        }
    }
}