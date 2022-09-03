using System;
using CSP.Events;
using CSP.Modules.Pages.MCU.Components;
using Prism.Mvvm;
using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Reflection;
using System.Xml.Serialization;
using Serilog;

namespace CSP.Modules.Pages.MCU.Models
{
    public class PinModel : BindableBase
    {
        private string _function;
        private bool _isLocked;
        private string _label = "";
        private string _name;
        private int _position;

        [ReadOnly(true)]
        [Display(Name = "功能", Description = "Pin 功能", GroupName = "系统")]
        [XmlAttribute]
        public string Function {
            get => _function;
            set => SetProperty(ref _function, value);
        }

        [ReadOnly(true)]
        [Display(Name = "锁定", Description = "锁定", GroupName = "基础")]
        [XmlAttribute]
        public bool IsLocked {
            get => _isLocked;
            set => SetProperty(ref _isLocked, value);
        }

        [ReadOnly(true)]
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

        public PropertyDetails Property { get; } = new();

        public IDictionary<string, Dictionary<string, Attribute>> GetAttributes() {
            var rtn = new Dictionary<string, Dictionary<string, Attribute>>();
            var infos = typeof(PinModel).GetProperties();
            foreach (var info in infos) {
                var attrs = info.GetCustomAttributes(false);
                if (attrs.Length > 0) {
                    var attributes = new Dictionary<string, Attribute>();
                    foreach (var attr in attrs) {
                        switch (attr) {
                            case DisplayAttribute displayAttribute: {
                                    if (displayAttribute.Name != null) {
                                        attributes.Add("DisplayName", new DisplayNameAttribute(displayAttribute.Name));
                                    }
                                    if (displayAttribute.Description != null) {
                                        attributes.Add("Description", new DescriptionAttribute(displayAttribute.Description));
                                    }
                                    if (displayAttribute.GroupName != null) {
                                        attributes.Add("Category", new CategoryAttribute(displayAttribute.GroupName));
                                    }
                                    break;
                                }
                            case ReadOnlyAttribute readOnlyAttribute: {
                                    attributes.Add("ReadOnly", new ReadOnlyAttribute(readOnlyAttribute.IsReadOnly));
                                    break;
                                }
                        }
                    }
                    rtn.Add(info.Name, attributes);
                }
            }

            return rtn;
        }

        public IDictionary<string, object> GetDetails() {
            var rtn = new Dictionary<string, object> {
                {"Function", Function},
                {"IsLocked", IsLocked},
                {"Label", Label},
                {"Name", Name},
                {"Position", Position},
            };

            return rtn;
        }
    }
}