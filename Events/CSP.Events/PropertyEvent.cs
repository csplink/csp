using Prism.Events;
using Prism.Mvvm;
using System.Collections.Generic;

namespace CSP.Events
{
    public class PropertyEvent : PubSubEvent<PropertyEvent.Model>
    {
        public class Model : BindableBase
        {
            public object Data { get; set; }
            public List<string> ShowList { get; set; } = new();
        }
    }
}