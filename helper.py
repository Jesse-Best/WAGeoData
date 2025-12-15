from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.PyQt.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import xml.etree.ElementTree as ET

class Helper(QObject):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, url, service):
        super().__init__()
        self.url = url
        self.service = service
        self.failed = False
        self.nam = QNetworkAccessManager()
        self.nam.finished.connect(self._reply)

    def fetch(self):
        req = QNetworkRequest(self.url)
        req.setRawHeader(b"User-Agent", b"Mozilla/5.0")
        self.nam.get(req)

    def _reply(self, reply):
        if reply.error() != QNetworkReply.NoError:
            message = f"Failed to fetch capabilities:\n{reply.errorString()}"
            self.failed = True
            self.error.emit(message)
            return
        data = reply.readAll().data()
        try:
            if self.service == "WMS":
                layers = self._parse_WMS(data)
                self.finished.emit(layers)
            elif self.service == "WFS":
                layers = self._parse_WFS(data)
                self.finished.emit(layers)
        except Exception as e:
            self.failed = True
            self.error.emit(f"Invalid GetCapabilities response:\n{e}")
        reply.deleteLater()

    def _parse_WMS(self, xml_bytes):
        root = ET.fromstring(xml_bytes)
        capability = root.find(".//{*}Capability")
        top_layer = capability.find(".//{*}Layer")
        results = []
        self._walk_WMS(top_layer, results)
        return results

    def _walk_WMS(self, elem, out):
        name = elem.find("{*}Name")
        title = elem.find("{*}Title")
        if name is not None:
            out.append((title.text if title is not None else name.text, name.text))
        for child in elem.findall("{*}Layer"):
            self._walk_WMS(child, out)

    def _parse_WFS(self, xml_bytes):
        root = ET.fromstring(xml_bytes)

        ft_list = root.find(".//{*}FeatureTypeList")
        if ft_list is None:
            raise ValueError("Not a valid WFS GetCapabilities document")

        results = []
        for ft in ft_list.findall("{*}FeatureType"):
            name = ft.find("{*}Name")
            title = ft.find("{*}Title")

            if name is not None:
                results.append((title.text if title is not None else name.text, name.text))

        return results