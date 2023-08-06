import os
import toml
from ..semver import prompt as semver_prompt
from .. import yaml_


def bump_version(
    semver_num: str = None,
    config_file: str = "pyproject.toml",
) -> str:

    file = config_file

    if not os.path.exists(file):
        file = "Project"
        print(f"Cannot find '{config_file}'. Falling back to '{file}'...")

    try:
        data = toml.load(file)
        data_type = "toml"
        version_in_file = data["mewo_project"]["version"]
    except toml.decoder.TomlDecodeError:
        data = yaml.loadfile(file)
        data_type = "yaml"
        version_in_file = data["version"]

    if not semver_num:
        semver_num = semver_prompt.semver_num_by_choice(version_in_file)

    if data_type == "toml":
        data["mewo_project"].update({"version": semver_num})
        with open(file, "w") as f:
            toml.dump(data, f)
    elif data_type == "yaml":
        data.update({"version": semver_num})
        yaml.savefile(data, file)

    return semver_num
