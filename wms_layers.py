import json
import os

file_name = os.path.dirname(__file__)+"\\wms_layers.json"

with open(file_name) as file:
    WMS_LAYERS = json.load(file)