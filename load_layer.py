from qgis.core import QgsRasterLayer, QgsVectorLayer, QgsProject, QgsNetworkAccessManager, Qgis

def load_layer(layer, service_url, iface, layer_format):
    if layer_format == "WMS":
        layer_name = layer[0]
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

        if not QgsNetworkAccessManager.instance().networkAccessible():
            iface.messageBar().pushMessage("WA Geo Data:", "Cannot load layer - no internet connection.", level=Qgis.Warning, duration=15)
            return
        
        map_layer = QgsRasterLayer(uri, layer_name, "wms")

        if not map_layer.isValid():
            iface.messageBar().pushMessage("WA Geo Data:", f"Failed to load WMS layer {layer_name}.", level=Qgis.Warning, duration=15)
            return
        
        QgsProject.instance().addMapLayer(map_layer)
        
    elif layer_format == "WFS":
        layer_name = layer[0].replace("_"," ").strip()
        uri = (
            f"typename='{layer[1]}'"
            f"url='{service_url}'"
        )

        if not QgsNetworkAccessManager.instance().networkAccessible():
            iface.messageBar().pushMessage("WA Geo Data:", "Cannot load layer - no internet connection.", level=Qgis.Warning, duration=15)
            return
        
        map_layer = QgsVectorLayer(uri, layer_name, "WFS")

        if not map_layer.isValid():
            iface.messageBar().pushMessage("WA Geo Data:", f"Failed to load WFS layer {layer_name}.", level=Qgis.Warning, duration=15)
            return
        
        QgsProject.instance().addMapLayer(map_layer)