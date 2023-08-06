from session import Session


class ChargeACH:
    def __init__(self, app, key, endpoint) -> None:
        self.app = app
        self.key = key
        self.endpoint = endpoint
        self.route = "/ach"

    def Process(self, request):
        # Create a session with the server
        session = Session(self.app, self.key, self.endpoint, self.route)

        accountType = "C"
        if "accountType" in request:
            accountType = request["accountType"]

        currency = "USD"
        if "currency" in request:
            currency = request["currency"]

        # Contruct charge ach packet
        req = {
            "account": request["account"],
            "routing": request["routing"],
            "accountType": accountType,
            "action": "A",
            "amount": request["amount"],
            "cardHolderName": request["accountHolder"],
            "currency": currency
        }

        return session.Send(req)
