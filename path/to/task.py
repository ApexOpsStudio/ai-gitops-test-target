import os
import yaml
from pathlib import Path

CONFIG_PATH = Path.home() / '.config' / 'task-cli' / 'config.yaml'

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        print(f"Configuration file not found at '{CONFIG_PATH}'. Creating a default config.")
        default_config = {
            'setting_1': 'default_value_1',
            'setting_2': 'default_value_2'
        }
        create_default_config(default_config)
        return default_config

    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)
        return config

def create_default_config(config: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        yaml.dump(config, f)
    print(f"Default configuration created at '{CONFIG_PATH}'.")

# ... rest of the code ...