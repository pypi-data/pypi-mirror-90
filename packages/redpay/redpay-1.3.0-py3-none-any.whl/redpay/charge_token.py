from session import Session


class ChargeToken:
    def __init__(self, app, key, endpoint) -> None:
        self.app = app
        self.key = key
        self.endpoint = endpoint
        self.route = "/ecard"

    def Process(self, request):
        # Create a session with the server
        session = Session(self.app, self.key, self.endpoint, self.route)

        # Contruct charge token packet
        req = {
            "token": request["token"],
            "action": "TA",
            "amount": request["amount"],
        }

        return session.Send(req)
