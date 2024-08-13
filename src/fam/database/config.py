import yaml


def load_config(config_file: str):
    """Load configuration from a YAML file."""
    with open(config_file, "r") as file:
        return yaml.safe_load(file)
