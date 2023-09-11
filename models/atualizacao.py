import requests

from requests.auth import HTTPDigestAuth

session = requests.Session()
digest = HTTPDigestAuth("c084029", "Iris2502")

session.post('http://' + "sipen.caixa", auth=digest)