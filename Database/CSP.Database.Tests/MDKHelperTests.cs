using CSP.Resources;
using System;
using System.IO;
using Xunit;
using Xunit.Abstractions;

namespace CSP.Database.Tests
{
    public class MDKHelperTests : IDisposable
    {
        private readonly ITestOutputHelper _testOutputHelper;

        public MDKHelperTests(ITestOutputHelper testOutputHelper)
        {
            _testOutputHelper = testOutputHelper;
        }

        public void Dispose()
        {
            IniFile.Save();
        }

        [Fact]
        public void Load()
        {
            var solutionDir = File.ReadAllLines("./SolutionDir.txt")[0];
            var path = $"{solutionDir}/Database/CSP.Database.Tests/test/STM32F401RE.uvprojx";
            var model = MDKHelper.Load(path);

            Assert.False(model == null);
            Assert.False(model.Targets == null);
            Assert.False(model.Targets.Length == 0);
        }
    }
}