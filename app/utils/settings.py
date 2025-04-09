import json
import os
from pathlib import Path

CONFIG_PATH = Path.home() / ".s3_uploader_config.json"

def save_config(data: dict):
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Failed to save config: {e}")

def load_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}
