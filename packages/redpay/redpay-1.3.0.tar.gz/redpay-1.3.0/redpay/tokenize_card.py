from session import Session


class TokenizeCard:
    def __init__(self, app, key, endpoint) -> None:
        self.app = app
        self.key = key
        self.endpoint = endpoint
        self.route = "/token"

    def Process(self, request):
        # Create a session with the server
        session = Session(self.app, self.key, self.endpoint, self.route)

        # Contruct tokenize card packet
        req = {
            "account": request["account"],
            "action": "T",
            "expmmyyyy": request["expmmyyyy"],
            "cvv": request["cvv"],
            "cardHolderName": request["accountHolder"],
            "avsZip": request["zipCode"]
        }

        return session.Send(req)
