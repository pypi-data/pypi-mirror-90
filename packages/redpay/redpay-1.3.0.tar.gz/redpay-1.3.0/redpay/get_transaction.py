import http.client
import json


class GetTransaction:
    def __init__(self, app, key, endpoint) -> None:
        self.app = app
        self.key = key
        self.endpoint = endpoint
        self.route = "/gettransaction"

    def Process(self, request):
        json_data = json.dumps(request)

        # POST Request
        conn = http.client.HTTPSConnection(self.endpoint)
        headers = {'Content-type': 'application/json'}

        # Send the request
        conn.request('POST', self.route, json_data, headers)
        response = json.loads(conn.getresponse().read().decode())

        return response
