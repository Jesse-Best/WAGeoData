from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.PyQt.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import xml.etree.ElementTree as ET

class Helper(QObject):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url
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
            layers = self._parse(data)
            self.finished.emit(layers)
        except Exception as e:
            self.failed = True
            self.error.emit(f"Invalid GetCapabilities response:\n{e}")
        reply.deleteLater()

    def _parse(self, xml_bytes):
        root = ET.fromstring(xml_bytes)
        capability = root.find(".//{*}Capability")
        top_layer = capability.find(".//{*}Layer")
        results = []
        self._walk(top_layer, results)
        return results

    def _walk(self, elem, out):
        name = elem.find("{*}Name")
        title = elem.find("{*}Title")
        if name is not None:
            out.append((title.text if title is not None else name.text,
                        name.text))
        for child in elem.findall("{*}Layer"):
            self._walk(child, out)


