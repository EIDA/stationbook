import gzip
from urllib.request import Request, urlopen
from ..logger import StationBookLoggerMixin

class DOIHelper(StationBookLoggerMixin):
    def __init__(self):
        super(DOIHelper, self).__init__()

    def get_network_doi(self, network_code, network_start_year):
        response = self._request('http://fdsn.org/networks/doi')
        decoded = response.decode('utf-8')
        dois = decoded.split('\n')
        doi = list(
            filter(
                lambda x: x.startswith(
                    f'{network_code}_{network_start_year}'
                ), dois
            )
        )
        return None

    def _request(self, url):
        try:
            req = Request(url)
            req.add_header('Accept-Encoding', 'gzip')
            response = urlopen(req)

            if response.info().get('Content-Encoding') == 'gzip':
                return gzip.decompress(response.read())
            else:
                return response.read()
        except Exception:
            self.log_exception(url)
            return None