from qgis.core import QgsRasterLayer, QgsVectorLayer, QgsProject, Qgis
import os
from .format_name import *

def load_layer(layer, service_url, iface, layer_format):
    if layer_format == "WMS":
        layer_name = format_name(layer[0])
        uri = (
            "contextualWMSLegend=0"
            "&version=1.3.0"
            "&crs=EPSG:7844"
            "&format=image/png"
            "&transparent=true"
            f"&layers={layer[1]}"
            "&styles="
            f"&url={service_url}"
        )
        
        map_layer = QgsRasterLayer(uri, layer_name, "wms")

        if not map_layer.isValid():
            iface.messageBar().pushMessage("WA Geo Data", f"Failed to load WMS layer {layer_name}.", level=Qgis.Warning, duration=15)
            return
        
        QgsProject.instance().addMapLayer(map_layer)
        
    elif layer_format == "WFS":
        layer_name = format_name(layer[0].replace("_"," ").strip())
        uri = (
            f"typename='{layer[1]}'"
            f"url='{service_url}'"
        )
        
        map_layer = QgsVectorLayer(uri, layer_name, "WFS")

        if not map_layer.isValid():
            iface.messageBar().pushMessage("WA Geo Data", f"Failed to load WFS layer {layer_name}.", level=Qgis.Warning, duration=15)
            return
        
        # applies .qml styles to WFS layer
        style_key = layer_name[-10:-1]
        qml_path = os.path.join(
            os.path.dirname(__file__),
            "resources",
            "styles",
            f"{style_key}.qml",
        )
        if os.path.exists(qml_path):
            map_layer.loadNamedStyle(qml_path)

        QgsProject.instance().addMapLayer(map_layer)
        map_layer.triggerRepaint()