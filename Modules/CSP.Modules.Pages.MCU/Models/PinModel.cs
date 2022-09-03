using Prism.Mvvm;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Xml.Serialization;

namespace CSP.Modules.Pages.MCU.Models
{
    public class PinModel : BindableBase
    {
        private string _function;
        private bool _isLocked;
        private string _label;
        private string _name;
        private int _position;

        [Display(Name = "功能", Description = "Pin 功能", GroupName = "系统")]
        [XmlAttribute]
        public string Function {
            get => _function;
            set => SetProperty(ref _function, value);
        }

        [Display(Name = "锁定", Description = "锁定", GroupName = "基础")]
        [XmlAttribute]
        public bool IsLocked {
            get => _isLocked;
            set => SetProperty(ref _isLocked, value);
        }

        [Display(Name = "标签", Description = "Pin 标签, 用于宏定义", GroupName = "基础")]
        [XmlAttribute]
        public string Label {
            get => _label;
            set => SetProperty(ref _label, value);
        }

        [ReadOnly(true)]
        [Display(Name = "名称", Description = "Pin 名称", GroupName = "基础")]
        [XmlAttribute]
        public string Name {
            get => _name;
            set => SetProperty(ref _name, value);
        }

        [ReadOnly(true)]
        [Display(Name = "引脚序号", Description = "Pin 引脚序号", GroupName = "基础")]
        [XmlAttribute]
        public int Position {
            get => _position;
            set => _ = SetProperty(ref _position, value);
        }
    }
}