#![allow(non_snake_case)]
#![allow(unused_assignments)]
#![allow(dead_code)]

use std::collections::HashMap as AttributeMap;
use std::fs::File;

use clap::{Parser};
use serde::{Deserialize, Serialize};
use serde_json::Result;
use xmltree::{Element, XMLNode};

mod template;

#[derive(Parser)]
struct Cli {
    /// Path to csp configuration
    #[clap(short, long)]
    csp: String,

    /// Path to output file
    #[clap(short, long, default_value = "./MDK-ARM")]
    output: String,

    /// MDK Version
    #[clap(short, long, default_value = "5.37", value_parser = ["5.37"])]
    version: String,


}

#[derive(Serialize, Deserialize)]
struct Core {
    company: String,
    hal: String,
    target: String,
    arch: String,
}

#[derive(Serialize, Deserialize)]
struct MdkArm {
    device: String,
    pack: String,
    pack_url: String,
    cmsis_core: String,
}

#[derive(Serialize, Deserialize)]
struct Csp {
    core: Core,
    mdk_arm: MdkArm,
    name: String,
}

#[derive(Serialize, Deserialize)]
struct Project {
    Defines: String,
    IncludePath: Vec<String>,
    CoreSrc: Vec<String>,
    LibSrc: Vec<String>,
}

struct DllOption {
    pub SimDllName: &'static str,
    pub SimDllArguments: &'static str,
    pub SimDlgDll: &'static str,
    pub SimDlgDllArguments: &'static str,
    pub TargetDllName: &'static str,
    pub TargetDllArguments: &'static str,
    pub TargetDlgDll: &'static str,
    pub TargetDlgDllArguments: &'static str,
}

impl DllOption {
    pub fn from(arch: &str) -> DllOption {
        match arch {
            "Arm Cortex-M3" => DllOption {
                SimDllName: "SARMCM3.DLL",
                SimDllArguments: "-REMAP",
                SimDlgDll: "DCM.DLL",
                SimDlgDllArguments: "-pCM3",
                TargetDllName: "SARMCM3.DLL",
                TargetDllArguments: "",
                TargetDlgDll: "TCM.DLL",
                TargetDlgDllArguments: "-pCM3",
            },
            "Arm Cortex-M0" | _ => DllOption {
                SimDllName: "SARMCM0.DLL",
                SimDllArguments: "-REMAP",
                SimDlgDll: "DCM.DLL",
                SimDlgDllArguments: "-pCM0",
                TargetDllName: "SARMCM0.DLL",
                TargetDllArguments: "",
                TargetDlgDll: "TCM.DLL",
                TargetDlgDllArguments: "-pCM0",
            },
        }
    }
}

struct Uvprojx {
    Define: String,
    IncludePath: String,
    wLevel: String,
}

fn load_csp_config(path: &str) -> Result<Csp> {
    let contents = std::fs::read_to_string(path)
        .expect("Something went wrong reading the file");

    let csp: Csp = serde_json::from_str(&contents)?;

    Ok(csp)
}

fn load_project_config(path: &str) -> Result<Project> {
    let contents = std::fs::read_to_string(path)
        .expect("Something went wrong reading the file");

    let project: Project = serde_json::from_str(&contents)?;

    Ok(project)
}

fn create_group(name: &str, files: Vec<String>) -> Result<Element> {
    let mut Group = Element::new("Group");
    let mut GroupName = Element::new("GroupName");
    GroupName.children.push(xmltree::XMLNode::Text(
        name.to_string()
    ));
    Group.children.push(xmltree::XMLNode::Element(GroupName));

    let mut Files = Element::new("Files");
    for file in files {
        let mut File = Element::new("File");

        let file_name = file.replace("\\", "/").split("/").last().unwrap().to_string();
        let mut FileName = Element::new("FileName");
        FileName.children.push(xmltree::XMLNode::Text(
            file_name
        ));

        File.children.push(xmltree::XMLNode::Element(FileName));

        // 检测后缀
        let suffix = file.split(".").last().unwrap();
        let file_type = match suffix {
            "c" | "C" => {
                "1"
            }
            "s" | "S" => {
                "2"
            }
            _ => {
                "0"
            }
        };

        let mut FileType = Element::new("FileType");
        FileType.children.push(xmltree::XMLNode::Text(
            file_type.to_string()
        ));
        File.children.push(xmltree::XMLNode::Element(FileType));

        let mut FilePath = Element::new("FilePath");
        FilePath.children.push(xmltree::XMLNode::Text(
            file
        ));
        File.children.push(xmltree::XMLNode::Element(FilePath));

        Files.children.push(xmltree::XMLNode::Element(File));
    }
    Group.children.push(xmltree::XMLNode::Element(Files));

    Ok(Group)
}

fn modify_uvprojx(body: &str, csp: &Csp, arg: &Cli) -> Result<()> {
    let mut root = Element::parse(body.as_bytes()).unwrap();

    let Target = root.get_mut_child("Targets").unwrap()
                         .get_mut_child("Target").unwrap();

    let TargetName = Target.get_child("TargetName").unwrap();
    if TargetName.get_text().is_none() {
        let TargetName = Target.get_mut_child("TargetName").unwrap();
        TargetName.children.push(xmltree::XMLNode::Text(
            csp.name.clone()
        ));
    }

    let uAC6 = Target.get_mut_child("uAC6").unwrap();
    uAC6.children = vec![xmltree::XMLNode::Text(
        "1".to_string()
    )];

    let TargetOption = Target.get_mut_child("TargetOption").unwrap();

    let TargetCommonOption = TargetOption.get_mut_child("TargetCommonOption").unwrap();

    let Device = TargetCommonOption.get_child("Device").unwrap();
    if Device.get_text().is_none() {
        let Device = TargetCommonOption.get_mut_child("Device").unwrap();
        Device.children.push(xmltree::XMLNode::Text(
            csp.mdk_arm.device.clone()
        ));

        let Vendor = TargetCommonOption.get_mut_child("Vendor").unwrap();
        Vendor.children.push(xmltree::XMLNode::Text(
            csp.core.company.clone()
        ));

        let mut PackID = Element::new("PackID");
        PackID.children.push(xmltree::XMLNode::Text(
            csp.mdk_arm.pack.clone()
        ));
        TargetCommonOption.children.push(xmltree::XMLNode::Element(PackID));

        let mut PackURL = Element::new("PackURL");
        PackURL.children.push(xmltree::XMLNode::Text(
            csp.mdk_arm.pack_url.clone()
        ));
        TargetCommonOption.children.push(xmltree::XMLNode::Element(PackURL));
    }

    let OutputDirectory = TargetCommonOption.get_child("OutputDirectory").unwrap();
    if OutputDirectory.get_text().is_none() {
        let OutputDirectory = TargetCommonOption.get_mut_child("OutputDirectory").unwrap();
        OutputDirectory.children.push(xmltree::XMLNode::Text(
            csp.name.clone() + "\\"
        ));

        let OutputName = TargetCommonOption.get_mut_child("OutputName").unwrap();
        OutputName.children.push(xmltree::XMLNode::Text(
            csp.name.clone()
        ));
    }

    let AfterMake = TargetCommonOption.get_mut_child("AfterMake").unwrap();
    let RunUserProg2 = AfterMake.get_mut_child("RunUserProg2").unwrap();
    RunUserProg2.children = vec![xmltree::XMLNode::Text(
        "1".to_string()
    )];

    let dllOption = DllOption::from(csp.core.arch.as_str());

    let DllOption = TargetOption.get_mut_child("DllOption").unwrap();
    let SimDllName = DllOption.get_child("SimDllName").unwrap();
    if SimDllName.get_text().is_none() {
        fn create_element(name: &str, text: &str) -> xmltree::XMLNode {
            xmltree::XMLNode::Element(
                Element {
                    name: name.to_string(),
                    prefix: None,
                    namespace: None,
                    namespaces: None,
                    attributes: AttributeMap::new(),
                    children: vec![xmltree::XMLNode::Text(text.to_string())],
                },
            )
        }

        let child = vec!(
            create_element("SimDllName", dllOption.SimDllName),
            create_element("SimDllArguments", dllOption.SimDllArguments),
            create_element("SimDlgDll", dllOption.SimDlgDll),
            create_element("SimDlgDllArguments", dllOption.SimDlgDllArguments),
            create_element("TargetDllName", dllOption.TargetDllName),
            create_element("TargetDllArguments", dllOption.TargetDllArguments),
            create_element("TargetDlgDll", dllOption.TargetDlgDll),
            create_element("TargetDlgDllArguments", dllOption.TargetDlgDllArguments),
        );
        DllOption.children = child;
    }

    let project_path = arg.output.clone() + "/temp.json";
    dbg!(project_path.clone());
    let project = load_project_config(&project_path).unwrap();

    let TargetArmAds = TargetOption.get_mut_child("TargetArmAds").unwrap();

    let Cads = TargetArmAds.get_mut_child("Cads").unwrap();

    let VariousControls = Cads.get_mut_child("VariousControls").unwrap();

    let Define = VariousControls.get_mut_child("Define").unwrap();
    if Define.get_text().is_none() {
        let Define = VariousControls.get_mut_child("Define").unwrap();
        Define.children.push(xmltree::XMLNode::Text(
            project.Defines.clone()
        ));
    } else {
        let old_define = Define.get_text().unwrap().into_owned();
        // 检测是否已经存在
        if !old_define.contains(&project.Defines) {
            let Define = VariousControls.get_mut_child("Define").unwrap();
            Define.children.push(xmltree::XMLNode::Text(
                ",".to_string() + &project.Defines
            ));
        }
    }

    let IncludePath = VariousControls.get_mut_child("IncludePath").unwrap();
    if IncludePath.get_text().is_none() {
        let IncludePath = VariousControls.get_mut_child("IncludePath").unwrap();
        IncludePath.children.push(xmltree::XMLNode::Text(
            project.IncludePath.join(";")
        ));
    } else {
        let old_include_path = IncludePath.get_text().unwrap().into_owned();
        // 检测是否已经存在
        if !old_include_path.contains(&project.IncludePath.join(";")) {
            let IncludePath = VariousControls.get_mut_child("IncludePath").unwrap();
            IncludePath.children.push(xmltree::XMLNode::Text(
                ";".to_string() + &project.IncludePath.join(";")
            ));
        }
    }

    let Groups = Target.get_mut_child("Groups").unwrap();
    let Groups_child = &Groups.children;

    let mut isCoreSrc = false;
    let mut isLibSrc = false;
    for group in Groups_child {
        match group {
            XMLNode::Element(e) => {
                let GroupName = e.get_child("GroupName").unwrap();
                if GroupName.get_text().is_none() {
                    continue;
                }
                let GroupName = GroupName.get_text().unwrap().into_owned();
                match GroupName.as_str() {
                    "CoreSrc" => {
                        isCoreSrc = true;
                    }
                    "LibSrc" => {
                        isLibSrc = true;
                    }
                    _ => {}
                }
            }
            _ => {}
        }
    }

    if !isCoreSrc {
        let CoreSrc = create_group("Core/Src", project.CoreSrc).unwrap();
        Groups.children.push(xmltree::XMLNode::Element(CoreSrc));
    }

    if !isLibSrc {
        let LibSrc = create_group("Libraries/Src", project.LibSrc).unwrap();
        Groups.children.push(xmltree::XMLNode::Element(LibSrc));
    }

    let mut path = arg.output.clone();
    path.push_str("/");
    path.push_str(&csp.name);
    path.push_str(".uvprojx");

    let dir = arg.output.clone();
    if !std::path::Path::new(&dir).exists() {
        std::fs::create_dir_all(&dir).unwrap();
    }
    let file = File::create(path).unwrap();

    root.write_with_config(file, xmltree::EmitterConfig::new()
        .perform_indent(true)
        .normalize_empty_elements(true),
    ).unwrap();

    Ok(())
}

fn main() {
    let args = Cli::parse();
    let csp = load_csp_config(&args.csp).unwrap();
    let mut template = String::from("");
    // 检测之前是否已经生成过
    let mut path = args.output.clone();
    path.push_str("/");
    path.push_str(&csp.name);
    path.push_str(".uvprojx");
    if std::path::Path::new(&path).exists() {
        template = std::fs::read_to_string(&path).unwrap();
    } else {
        // 读取模板
        let template_path = template::Asset::get(format!("{}/template.uvprojx", args.version.as_str()).as_str()).unwrap();
        template = String::from_utf8(template_path.data.to_vec()).unwrap();
    }

    modify_uvprojx(&template, &csp, &args).unwrap();
}