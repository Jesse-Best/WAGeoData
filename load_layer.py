from qgis.core import QgsRasterLayer, QgsProject, QgsNetworkAccessManager, Qgis

def load_layer(self, layer, service_url, iface):

    layer_name = layer[0]
    uri = (
        f"contextualWMSLegend=0"
        f"&crs=EPSG:4326"
        f"&dpiMode=7"
        f"&featureCount=10"
        f"&format=image/jpeg"
        f"&layers={layer[1]}"
        f"&styles"
        f"&tilePixelRatio=0"
        f"&url={service_url}"
    )

    if QgsNetworkAccessManager.instance().networkAccessible():
        map_layer = QgsRasterLayer(uri, layer_name, "wms")
        QgsProject.instance().addMapLayer(map_layer)
    else:
        iface.messageBar().pushMessage("WA Geo Data:", "Cannot load layer - no internet connection.", level=Qgis.Warning, duration=15)
    return

    