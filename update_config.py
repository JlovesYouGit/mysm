import json
import os

# Path to the config.json file
config_path = r"N:\sms\venv\Lib\site-packages\rtlsdr\config.json"

# New configuration with full paths
new_config = {
    "x64": r"N:\sms\Release\x64\rtlsdr.dll",
    "x86": r"N:\sms\Release\x64\rtlsdr.dll"
}

# Write the new configuration
with open(config_path, 'w') as f:
    json.dump(new_config, f, indent=2)

print("Config file updated successfully!")
print(f"New config: {new_config}")