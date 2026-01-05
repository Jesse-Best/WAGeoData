from qgis.PyQt.QtCore import QObject, pyqtSignal, QUrl
from qgis.PyQt.QtNetwork import QNetworkReply
from qgis.core import QgsNetworkContentFetcher
import xml.etree.ElementTree as ET

class Helper(QObject):
    finished = pyqtSignal(list, name="finished")
    error = pyqtSignal(str, name="error")

    def __init__(self, url, service):
        super().__init__()
        self.url = url
        self.service = service
        self.failed = False
        self.fetcher = None

    def fetch(self):
        self.fetcher = QgsNetworkContentFetcher()
        self.fetcher.setParent(self)
        self.fetcher.finished.connect(self._reply)
        self.fetcher.fetchContent(QUrl(self.url))

    def _reply(self):
        if not self.fetcher:
            return
            
        # check for errors
        reply = self.fetcher.reply()
        if not reply:
            self.failed = True
            self.error.emit(f"Failed to fetch capabilities:\nNo reply object created")
            return
        try:
            no_error = QNetworkReply.NoError
        except AttributeError:
            no_error = QNetworkReply.NetworkError.NoError
        if reply.error() != no_error:
            error_code = reply.error()
            error_msg = reply.errorString() if hasattr(reply, 'errorString') else "Unknown error"
            self.failed = True
            self.error.emit(f"Failed to fetch capabilities:\nError {error_code}: {error_msg}")
            return
        
        # read content as bytes
        try:
            data = bytes(self.fetcher.reply().content())
        except (AttributeError, TypeError):
            try:
                data = self.fetcher.reply().readAll().data()
            except (AttributeError, TypeError):
                # string fallback
                data = self.fetcher.reply().readAll()
        
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
    