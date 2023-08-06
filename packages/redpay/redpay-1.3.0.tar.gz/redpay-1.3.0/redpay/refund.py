from session import Session


class Refund:
    def __init__(self, app, key, endpoint) -> None:
        self.app = app
        self.key = key
        self.endpoint = endpoint
        self.route = "/ecard"

    def Process(self, request):
        # Create a session with the server
        session = Session(self.app, self.key, self.endpoint, self.route)

        # Contruct refund packet
        req = {
            "transactionId": request["transactionId"],
            "action": "R"
        }

        return session.Send(req)
