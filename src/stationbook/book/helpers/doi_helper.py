import gzip
import json
from urllib.request import Request, urlopen
from django.core.cache import cache
from ..logger import StationBookLoggerMixin
from datetime import date


class DOIHelper(StationBookLoggerMixin):
    def __init__(self):
        super(DOIHelper, self).__init__()

    def get_network_doi(self, network_code, network_start_year):
        try:
            dois = None

            if not cache.get("network_dois"):
                response = self._request("http://fdsn.org/ws/networks/1/query")
                dois = {}
                for net in response["networks"]:
                    network_key = net["fdsn_code"][:]
                    if net["end_date"]:
                        start_year = date.fromisoformat(net["start_date"]).strftime("%Y")
                        network_key = network_key + "_{}".format(start_year)

                    dois[network_key] = net["doi"]
                cache.set("network_dois", dois, 86400)
            else:
                dois = cache.get("network_dois")

            # Filter using network code and maybe network start year
            doi = dois.get(network_code)
            if doi is None:
                doi = dois.get("{}_{}".format(network_code, network_start_year))

            if not doi:
                return None

            doi = "https://www.doi.org/{}".format(doi)
            return doi
        except Exception as e:
            self.log_exception(e)
            return None

    def _request(self, url):
        try:
            req = Request(url)
            req.add_header("Accept-Encoding", "gzip")
            response = urlopen(req)

            if response.info().get("Content-Encoding") == "gzip":
                return gzip.decompress(response.read())
            elif response.headers.get('content-type') == 'application/json':
                return json.loads(response.read())
            else:
                return response.read()
        except Exception:
            self.log_exception(url)
            return None
