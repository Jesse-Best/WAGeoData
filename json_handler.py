import json
import os

plugin_dir = os.path.dirname(__file__)

file_name = os.path.join(plugin_dir, "resources", "json", "wms_layers.json")
with open(file_name) as file:
    WMS_LAYERS = json.load(file)

file_name = os.path.join(plugin_dir, "resources", "json", "excluded_services.json")
with open(file_name) as file:
    EXCLUDED_SERVICES = []
    temp = json.load(file)
    for entry in temp:
        EXCLUDED_SERVICES.append(entry["Service"])

file_name = os.path.join(plugin_dir, "resources", "json", "formatted_layers.json")
with open(file_name) as file:
    FORMATTED_LAYERS = json.load(file)