import os
import yaml

CONFIG_DIR = os.path.expanduser("~/.config/task-cli")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.yaml")

def load_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        create_default_config()
        print(f"Default configuration created at {CONFIG_PATH}. Please configure it.")
        return {}

    try:
        with open(CONFIG_PATH, 'r') as f:
            config_data = yaml.safe_load(f)
            return config_data or {}
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        return {}

def create_default_config() -> None:
    os.makedirs(CONFIG_DIR, exist_ok=True)
    default_config = {
        "setting1": "value1",
        "setting2": "value2"
    }
    with open(CONFIG_PATH, 'w') as f:
        yaml.dump(default_config, f)

if __name__ == "__main__":
    config = load_config()
    if config:
        # Proceed with application logic using the loaded config
        print("Configuration loaded successfully.")