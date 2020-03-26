import gzip
from urllib.request import Request, urlopen
from django.core.cache import cache
from ..logger import StationBookLoggerMixin


class DOIHelper(StationBookLoggerMixin):
    def __init__(self):
        super(DOIHelper, self).__init__()

    def get_network_doi(self, network_code, network_start_year):
        dois = None

        if not cache.get('network_dois'):
            response = self._request('http://fdsn.org/networks/doi')
            decoded = response.decode('utf-8')
            dois = decoded.split('\r\n')
            cache.set('network_dois', dois, 86400)
        else:
            dois = cache.get('network_dois')

        # Filter using network code and network start year
        doi = list(
            filter(
                lambda x: x.startswith(
                    '{}_{}'.format(network_code, network_start_year)
                ), dois
            )
        )

        # In case previous filter did not return any results, use less
        # restrictive filtering using just the network code
        # NL network falls in this category, for example
        if len(doi) <= 0:
            doi = list(
                filter(
                    lambda x: x.startswith(
                        '{}'.format(network_code)
                    ), dois
                )
            )

        doi = doi[0].split(',')[1]
        doi = 'https://www.doi.org/{}'.format(doi)
        return doi

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
