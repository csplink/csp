import yaml
import os
from package import *

dir_artifact = os.path.dirname(__file__) + "/artifact"
file_artifact = dir_artifact + "/artifact.xaml"
file_config = os.path.abspath(os.path.dirname(__file__) + "/config/package.yml")
packages = ["LQFP", "LFBGA"]

if not os.path.exists(dir_artifact):
    os.makedirs(dir_artifact)


def main():
    string = ""
    if not os.path.exists(file_config):
        raise OSError("the file: {file} is not exists.".format(file=file_config))
    with open(file_config, "r") as fp:
        string = fp.read()
    config = yaml.load(string, Loader=yaml.FullLoader)
    for name, item in config.items():
        if item["type"] in packages:
            action = item["type"].lower() + ".generate_" + item["type"].lower()
            data = eval(action)(name, item)
            with open(file_artifact, "w") as fp:
                fp.write(data)
        else:
            raise ValueError("please use correct type")


if __name__ == "__main__":
    main()
