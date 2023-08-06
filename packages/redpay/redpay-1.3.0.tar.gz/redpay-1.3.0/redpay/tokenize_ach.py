from session import Session


class TokenizeACH:
    def __init__(self, app, key, endpoint) -> None:
        self.app = app
        self.key = key
        self.endpoint = endpoint
        self.route = "/token"

    def Process(self, request):
        # Create a session with the server
        session = Session(self.app, self.key, self.endpoint, self.route)

        # Contruct tokenize ach packet
        req = {
            "account": request["account"],
            "routing": request["routing"],
            "action": "T",
            "cardHolderName": request["accountHolder"],
            "method": "ACH"
        }

        return session.Send(req)
