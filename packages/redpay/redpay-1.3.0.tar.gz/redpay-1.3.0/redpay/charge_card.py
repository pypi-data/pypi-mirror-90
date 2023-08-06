from session import Session


class ChargeCard:
    def __init__(self, app, key, endpoint) -> None:
        self.app = app
        self.key = key
        self.endpoint = endpoint
        self.route = "/ecard"

    def Process(self, request):
        # Create a session with the server
        session = Session(self.app, self.key, self.endpoint, self.route)

        # Contruct charge card packet
        req = {
            "account": request["account"],
            "action": "A",
            "amount": request["amount"],
            "expmmyyyy": request["expmmyyyy"],
            "cvv": request["cvv"],
            "cardHolderName": request["accountHolder"],
            "avsZip": request["zipCode"]
        }

        return session.Send(req)
