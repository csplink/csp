using System.Xml.Serialization;

namespace CSP.Modules.Pages.MCU.Models.Description
{
    [XmlRoot("Clock", IsNullable = false)]
    public class ClockModel
    {
        [XmlIgnore]
        public ControlModel Controls { get; set; }

        [XmlArray("Controls")]
        [XmlArrayItem("Control")]
        public ControlModel ControlsTemp { get; set; }

        [XmlAttribute]
        public float Height { get; set; }

        [XmlIgnore]
        public RectModel Rects { get; set; }

        [XmlArray("Rects")]
        [XmlArrayItem("Rect")]
        public RectModel RectsTemp { get; set; }

        [XmlAttribute]
        public float Width { get; set; }

        public class ControlModel
        {
            [XmlAttribute]
            public int ID { get; set; }

            [XmlAttribute]
            public string Name { get; set; }

            [XmlAttribute]
            public string Type { get; set; }
        }

        public class RectModel
        {
            [XmlAttribute]
            public float Height { get; set; }

            [XmlAttribute]
            public int ID { get; set; }

            [XmlAttribute]
            public float Width { get; set; }

            [XmlAttribute]
            public float X { get; set; }

            [XmlAttribute]
            public float Y { get; set; }
        }
    }
}