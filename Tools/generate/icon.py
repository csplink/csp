import os
import pathlib

template_icon_data = """
        public static BitmapImage {name} {{
            get => Instance.{name};
        }}
"""

template_icon_instance_data = "        internal readonly BitmapImage {name} = new(new Uri(@\"pack://application:,,,/CSP.Resources;component/Icon/{name}.png\"));\n"

template_icon_instance = """using System;
using System.Windows.Media.Imaging;

namespace CSP.Resources
{{
    internal class IconInstance
    {{
{data}    }}
}}"""

template_icon = """using System.Windows.Media.Imaging;

namespace CSP.Resources
{{
    public static class Icon
    {{
        private static readonly IconInstance Instance = new();
{data}    }}
}}"""

dir_resources = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "/Resources/CSP.Resources"
dir_resources_icon = dir_resources + "/Icon"
path_resources_icon = dir_resources + "/Icon.cs"
path_resources_icon_instance = dir_resources + "/IconInstance.cs"


def main():
    data_icon_instance = ""
    data_icon = ""
    p = pathlib.Path(dir_resources_icon)
    ret = p.glob("*.png")
    for item in ret:
        name = str(item.name).replace(".png", "")
        data_icon_instance += template_icon_instance_data.format(name=name)
        data_icon += template_icon_data.format(name=name)
    icon_instance = template_icon_instance.format(data=data_icon_instance)
    icon = template_icon.format(data=data_icon)

    with open(path_resources_icon_instance, "w", encoding="utf-8") as fp:
        fp.write(icon_instance)

    with open(path_resources_icon, "w", encoding="utf-8") as fp:
        fp.write(icon)


if __name__ == "__main__":
    main()
