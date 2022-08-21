using CSP.Utils;
using CSP.Utils.Extensions;
using System;
using System.IO;
using System.Windows;
using System.Xml.Serialization;

// ReSharper disable IdentifierTypo
// ReSharper disable InconsistentNaming

namespace CSP.Database.Models.MDK
{
    [XmlRoot("Project", IsNullable = false)]
    public class UvprojxModel
    {
        public string SchemaVersion { get; set; }

        public string Header { get; set; }

        [XmlArray("Targets")]
        [XmlArrayItem("Target")]
        public TargetModel[] Targets { get; set; }

        public RTEModel RTE { get; set; }

        public LayerInfoModel LayerInfo { get; set; }

        internal static UvprojxModel Load(string path)
        {
            DebugUtil.Assert(!path.IsNullOrEmpty(), new ArgumentNullException(nameof(path)));

            if (!File.Exists(path))
                return null;

            var deserializer = new XmlSerializer(typeof(UvprojxModel));
            var reader = new StreamReader(path);

            UvprojxModel rtn;
            try
            {
                rtn = (UvprojxModel)deserializer.Deserialize(reader);
            }
            catch (InvalidOperationException e)
            {
                MessageBox.Show(e.Message, "错误", MessageBoxButton.OK, MessageBoxImage.Error);
                return null;
            }

            DebugUtil.Assert(rtn != null, new ArgumentNullException(nameof(rtn)), "XML反序列化失败");
            if (rtn == null)
                return null;

            DebugUtil.Assert(rtn.Targets.Length >= 1, new ArgumentOutOfRangeException(nameof(rtn.Targets)));
            DebugUtil.Assert(rtn.RTE.components.Length >= 1, new ArgumentOutOfRangeException(nameof(rtn.RTE.components)));

            var targetInfos = rtn.RTE.components[0].targetInfos;
            DebugUtil.Assert(targetInfos.Length >= 1, new ArgumentOutOfRangeException(nameof(targetInfos)));

            var layers = rtn.LayerInfo.Layers;
            DebugUtil.Assert(layers.Length >= 1, new ArgumentOutOfRangeException(nameof(layers)));

            return rtn;
        }

        internal static UvprojxModel ChangeProjectName(UvprojxModel project, string dest)
        {
            project.Targets[0].TargetName = dest;
            project.Targets[0].TargetOption.TargetCommonOption.OutputName = dest;

            if (project.Targets[0].TargetOption.TargetArmAds.LDads.umfTarg == "1")
                project.Targets[0].TargetOption.TargetArmAds.LDads.ScatterFile = $".\\Objects\\{dest}.sct";

            foreach (var component in project.RTE.components)
                component.targetInfos[0].name = dest;

            project.LayerInfo.Layers[0].LayName = dest;

            return project;
        }

        public class TargetModel
        {
            public string TargetName { get; set; }

            public string ToolsetNumber { get; set; }

            public string ToolsetName { get; set; }

            public string pCCUsed { get; set; }

            public string uAC6 { get; set; }

            public TargetOptionModel TargetOption { get; set; }

            [XmlArray("Groups")]
            [XmlArrayItem("Group")]
            public GroupModel[] Groups { get; set; }

            public class TargetOptionModel
            {
                public TargetCommonOptionModel TargetCommonOption { get; set; }

                public CommonPropertyModel CommonProperty { get; set; }

                public DllOptionModel DllOption { get; set; }

                public DebugOptionModel DebugOption { get; set; }

                public UtilitiesModel Utilities { get; set; }

                public TargetArmAdsModel TargetArmAds { get; set; }

                public class TargetCommonOptionModel
                {
                    public string Device { get; set; }

                    public string Vendor { get; set; }

                    public string PackID { get; set; }

                    public string PackURL { get; set; }

                    public string Cpu { get; set; }

                    public string FlashUtilSpec { get; set; }

                    public string StartupFile { get; set; }

                    public string FlashDriverDll { get; set; }

                    public string DeviceId { get; set; }

                    public string RegisterFile { get; set; }

                    public string MemoryEnv { get; set; }

                    public string Cmp { get; set; }

                    public string Asm { get; set; }

                    public string Linker { get; set; }

                    public string OHString { get; set; }

                    public string InfinionOptionDll { get; set; }

                    public string SLE66CMisc { get; set; }

                    public string SLE66AMisc { get; set; }

                    public string SLE66LinkerMisc { get; set; }

                    public string SFDFile { get; set; }

                    public string bCustSvd { get; set; }

                    public string UseEnv { get; set; }

                    public string BinPath { get; set; }

                    public string IncludePath { get; set; }

                    public string LibPath { get; set; }

                    public string RegisterFilePath { get; set; }

                    public string DBRegisterFilePath { get; set; }

                    public TargetStatusModel TargetStatus { get; set; }

                    public string OutputDirectory { get; set; }

                    public string OutputName { get; set; }

                    public string CreateExecutable { get; set; }

                    public string CreateLib { get; set; }

                    public string CreateHexFile { get; set; }

                    public string DebugInformation { get; set; }

                    public string BrowseInformation { get; set; }

                    public string ListingPath { get; set; }

                    public string HexFormatSelection { get; set; }

                    public string Merge32K { get; set; }

                    public string CreateBatchFile { get; set; }

                    public BeforeCompileModel BeforeCompile { get; set; }

                    public BeforeMakeModel BeforeMake { get; set; }

                    public AfterMakeModel AfterMake { get; set; }

                    public string SelectedForBatchBuild { get; set; }

                    public string SVCSIdString { get; set; }

                    public class TargetStatusModel
                    {
                        public string Error { get; set; }

                        public string ExitCodeStop { get; set; }

                        public string ButtonStop { get; set; }

                        public string NotGenerated { get; set; }

                        public string InvalidFlash { get; set; }
                    }

                    public class BeforeCompileModel
                    {
                        public string RunUserProg1 { get; set; }

                        public string RunUserProg2 { get; set; }

                        public string UserProg1Name { get; set; }

                        public string UserProg2Name { get; set; }

                        public string UserProg1Dos16Mode { get; set; }

                        public string UserProg2Dos16Mode { get; set; }

                        public string nStopU1X { get; set; }

                        public string nStopU2X { get; set; }
                    }

                    public class BeforeMakeModel
                    {
                        public string RunUserProg1 { get; set; }

                        public string RunUserProg2 { get; set; }

                        public string UserProg1Name { get; set; }

                        public string UserProg2Name { get; set; }

                        public string UserProg1Dos16Mode { get; set; }

                        public string UserProg2Dos16Mode { get; set; }

                        public string nStopB1X { get; set; }

                        public string nStopB2X { get; set; }
                    }

                    public class AfterMakeModel
                    {
                        public string RunUserProg1 { get; set; }

                        public string RunUserProg2 { get; set; }

                        public string UserProg1Name { get; set; }

                        public string UserProg2Name { get; set; }

                        public string UserProg1Dos16Mode { get; set; }

                        public string UserProg2Dos16Mode { get; set; }

                        public string nStopA1X { get; set; }

                        public string nStopA2X { get; set; }
                    }
                }

                public class CommonPropertyModel
                {
                    public string UseCPPCompiler { get; set; }

                    public string RVCTCodeConst { get; set; }

                    public string RVCTZI { get; set; }

                    public string RVCTOtherData { get; set; }

                    public string ModuleSelection { get; set; }

                    public string IncludeInBuild { get; set; }

                    public string AlwaysBuild { get; set; }

                    public string GenerateAssemblyFile { get; set; }

                    public string AssembleAssemblyFile { get; set; }

                    public string PublicsOnly { get; set; }

                    public string StopOnExitCode { get; set; }

                    public string CustomArgument { get; set; }

                    public string IncludeLibraryModules { get; set; }

                    public string ComprImg { get; set; }
                }

                public class DllOptionModel
                {
                    public string SimDllName { get; set; }

                    public string SimDllArguments { get; set; }

                    public string SimDlgDll { get; set; }

                    public string SimDlgDllArguments { get; set; }

                    public string TargetDllName { get; set; }

                    public string TargetDllArguments { get; set; }

                    public string TargetDlgDll { get; set; }

                    public string TargetDlgDllArguments { get; set; }
                }

                public class DebugOptionModel
                {
                    public OPTHXModel OPTHX { get; set; }

                    public class OPTHXModel
                    {
                        public string HexSelection { get; set; }

                        public string HexRangeLowAddress { get; set; }

                        public string HexRangeHighAddress { get; set; }

                        public string HexOffset { get; set; }

                        public string Oh166RecLen { get; set; }
                    }
                }

                public class UtilitiesModel
                {
                    public Flash1Model Flash1 { get; set; }

                    public string bUseTDR { get; set; }

                    public string Flash2 { get; set; }

                    public string Flash3 { get; set; }

                    public string Flash4 { get; set; }

                    public string pFcarmOut { get; set; }

                    public string pFcarmGrp { get; set; }

                    public string pFcArmRoot { get; set; }

                    public string FcArmLst { get; set; }

                    public class Flash1Model
                    {
                        public string UseTargetDll { get; set; }

                        public string UseExternalTool { get; set; }

                        public string RunIndependent { get; set; }

                        public string UpdateFlashBeforeDebugging { get; set; }

                        public string Capability { get; set; }

                        public string DriverSelection { get; set; }
                    }
                }

                public class TargetArmAdsModel
                {
                    public ArmAdsMiscModel ArmAdsMisc { get; set; }

                    public CadsModel Cads { get; set; }

                    public AadsModel Aads { get; set; }

                    public LDadsModel LDads { get; set; }

                    public class ArmAdsMiscModel
                    {
                        public string GenerateListings { get; set; }

                        public string asHll { get; set; }

                        public string asAsm { get; set; }

                        public string asMacX { get; set; }

                        public string asSyms { get; set; }

                        public string asFals { get; set; }

                        public string asDbgD { get; set; }

                        public string asForm { get; set; }

                        public string ldLst { get; set; }

                        public string ldmm { get; set; }

                        public string ldXref { get; set; }

                        public string BigEnd { get; set; }

                        public string AdsALst { get; set; }

                        public string AdsACrf { get; set; }

                        public string AdsANop { get; set; }

                        public string AdsANot { get; set; }

                        public string AdsLLst { get; set; }

                        public string AdsLmap { get; set; }

                        public string AdsLcgr { get; set; }

                        public string AdsLsym { get; set; }

                        public string AdsLszi { get; set; }

                        public string AdsLtoi { get; set; }

                        public string AdsLsun { get; set; }

                        public string AdsLven { get; set; }

                        public string AdsLsxf { get; set; }

                        public string RvctClst { get; set; }

                        public string GenPPlst { get; set; }

                        public string AdsCpuType { get; set; }

                        public string RvctDeviceName { get; set; }

                        public string mOS { get; set; }

                        public string uocRom { get; set; }

                        public string uocRam { get; set; }

                        public string hadIROM { get; set; }

                        public string hadIRAM { get; set; }

                        public string hadXRAM { get; set; }

                        public string uocXRam { get; set; }

                        public string RvdsVP { get; set; }

                        public string RvdsMve { get; set; }

                        public string RvdsCdeCp { get; set; }

                        public string nBranchProt { get; set; }

                        public string hadIRAM2 { get; set; }

                        public string hadIROM2 { get; set; }

                        public string StupSel { get; set; }

                        public string useUlib { get; set; }

                        public string EndSel { get; set; }

                        public string uLtcg { get; set; }

                        public string nSecure { get; set; }

                        public string RoSelD { get; set; }

                        public string RwSelD { get; set; }

                        public string CodeSel { get; set; }

                        public string OptFeed { get; set; }

                        public string NoZi1 { get; set; }

                        public string NoZi2 { get; set; }

                        public string NoZi3 { get; set; }

                        public string NoZi4 { get; set; }

                        public string NoZi5 { get; set; }

                        public string Ro1Chk { get; set; }

                        public string Ro2Chk { get; set; }

                        public string Ro3Chk { get; set; }

                        public string Ir1Chk { get; set; }

                        public string Ir2Chk { get; set; }

                        public string Ra1Chk { get; set; }

                        public string Ra2Chk { get; set; }

                        public string Ra3Chk { get; set; }

                        public string Im1Chk { get; set; }

                        public string Im2Chk { get; set; }

                        public OnChipMemoriesModel OnChipMemories { get; set; }

                        public string RvctStartVector { get; set; }

                        public class OnChipMemoriesModel
                        {
                            public Ocm1Model Ocm1 { get; set; }

                            public Ocm2Model Ocm2 { get; set; }

                            public Ocm3Model Ocm3 { get; set; }

                            public Ocm4Model Ocm4 { get; set; }

                            public Ocm5Model Ocm5 { get; set; }

                            public Ocm6Model Ocm6 { get; set; }

                            public IRAMModel IRAM { get; set; }

                            public IROMModel IROM { get; set; }

                            public XRAMModel XRAM { get; set; }

                            public OCR_RVCT1Model OCR_RVCT1 { get; set; }

                            public OCR_RVCT2Model OCR_RVCT2 { get; set; }

                            public OCR_RVCT3Model OCR_RVCT3 { get; set; }

                            public OCR_RVCT4Model OCR_RVCT4 { get; set; }

                            public OCR_RVCT5Model OCR_RVCT5 { get; set; }

                            public OCR_RVCT6Model OCR_RVCT6 { get; set; }

                            public OCR_RVCT7Model OCR_RVCT7 { get; set; }

                            public OCR_RVCT8Model OCR_RVCT8 { get; set; }

                            public OCR_RVCT9Model OCR_RVCT9 { get; set; }

                            public OCR_RVCT10Model OCR_RVCT10 { get; set; }

                            public class Ocm1Model
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }

                            public class Ocm2Model
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }

                            public class Ocm3Model
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }

                            public class Ocm4Model
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }

                            public class Ocm5Model
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }

                            public class Ocm6Model
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }

                            public class IRAMModel
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }

                            public class IROMModel
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }

                            public class XRAMModel
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }

                            public class OCR_RVCT1Model
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }

                            public class OCR_RVCT2Model
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }

                            public class OCR_RVCT3Model
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }

                            public class OCR_RVCT4Model
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }

                            public class OCR_RVCT5Model
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }

                            public class OCR_RVCT6Model
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }

                            public class OCR_RVCT7Model
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }

                            public class OCR_RVCT8Model
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }

                            public class OCR_RVCT9Model
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }

                            public class OCR_RVCT10Model
                            {
                                public string Type { get; set; }

                                public string StartAddress { get; set; }

                                public string Size { get; set; }
                            }
                        }
                    }

                    public class CadsModel
                    {
                        public string interw { get; set; }

                        public string Optim { get; set; }

                        public string oTime { get; set; }

                        public string SplitLS { get; set; }

                        public string OneElfS { get; set; }

                        public string Strict { get; set; }

                        public string EnumInt { get; set; }

                        public string PlainCh { get; set; }

                        public string Ropi { get; set; }

                        public string Rwpi { get; set; }

                        public string wLevel { get; set; }

                        public string uThumb { get; set; }

                        public string uSurpInc { get; set; }

                        public string uC99 { get; set; }

                        public string uGnu { get; set; }

                        public string useXO { get; set; }

                        public string v6Lang { get; set; }

                        public string v6LangP { get; set; }

                        public string vShortEn { get; set; }

                        public string vShortWch { get; set; }

                        public string v6Lto { get; set; }

                        public string v6WtE { get; set; }

                        public string v6Rtti { get; set; }

                        public VariousControls1Model VariousControls { get; set; }

                        public class VariousControls1Model
                        {
                            public string MiscControls { get; set; }

                            public string Define { get; set; }

                            public string Undefine { get; set; }

                            public string IncludePath { get; set; }
                        }
                    }

                    public class AadsModel
                    {
                        public string interw { get; set; }

                        public string Ropi { get; set; }

                        public string Rwpi { get; set; }

                        public string thumb { get; set; }

                        public string SplitLS { get; set; }

                        public string SwStkChk { get; set; }

                        public string NoWarn { get; set; }

                        public string uSurpInc { get; set; }

                        public string useXO { get; set; }

                        public string ClangAsOpt { get; set; }

                        public VariousControls2Model VariousControls { get; set; }

                        public class VariousControls2Model
                        {
                            public string MiscControls { get; set; }

                            public string Define { get; set; }

                            public string Undefine { get; set; }

                            public string IncludePath { get; set; }
                        }
                    }

                    public class LDadsModel
                    {
                        public string umfTarg { get; set; }

                        public string Ropi { get; set; }

                        public string Rwpi { get; set; }

                        public string noStLib { get; set; }

                        public string RepFail { get; set; }

                        public string useFile { get; set; }

                        public string TextAddressRange { get; set; }

                        public string DataAddressRange { get; set; }

                        public string pXoBase { get; set; }

                        public string ScatterFile { get; set; }

                        public string IncludeLibs { get; set; }

                        public string IncludeLibsPath { get; set; }

                        public string Misc { get; set; }

                        public string LinkerInputFile { get; set; }

                        public string DisabledWarnings { get; set; }
                    }
                }
            }

            public class GroupModel
            {
                public string GroupName { get; set; }

                [XmlArray("Files")]
                [XmlArrayItem("File")]
                public File1Model[] Files { get; set; }

                public class File1Model
                {
                    public string FileName { get; set; }

                    public string FileType { get; set; }

                    public string FilePath { get; set; }
                }
            }
        }

        public class RTEModel
        {
            [XmlArray("apis")]
            [XmlArrayItem("api")]
            public ApiModel[] apis { get; set; }

            [XmlArray("components")]
            [XmlArrayItem("component")]
            public ComponentModel[] components { get; set; }

            [XmlArray("files")]
            [XmlArrayItem("file")]
            public File2Model[] files { get; set; }

            public class ComponentModel
            {
                [XmlAttribute]
                public string Cclass { get; set; }

                [XmlAttribute]
                public string Cgroup { get; set; }

                [XmlAttribute]
                public string Cvendor { get; set; }

                [XmlAttribute]
                public string Cversion { get; set; }

                [XmlAttribute]
                public string condition { get; set; }

                public PackageModel package { get; set; }

                [XmlArray("targetInfos")]
                [XmlArrayItem("targetInfo")]
                public TargetInfoModel[] targetInfos { get; set; }

                public class PackageModel
                {
                    [XmlAttribute]
                    public string name { get; set; }

                    [XmlAttribute]
                    public string schemaVersion { get; set; }

                    [XmlAttribute]
                    public string url { get; set; }

                    [XmlAttribute]
                    public string vendor { get; set; }

                    [XmlAttribute]
                    public string version { get; set; }
                }

                public class TargetInfoModel
                {
                    [XmlAttribute]
                    public string name { get; set; }
                }
            }

            public class ApiModel
            {
            }

            public class File2Model
            {
            }
        }

        public class LayerInfoModel
        {
            [XmlArray("Layers")]
            [XmlArrayItem("Layer")]
            public LayerModel[] Layers { get; set; }

            public class LayerModel
            {
                public string LayName { get; set; }

                public string LayPrjMark { get; set; }
            }
        }
    }
}