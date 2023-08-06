from charge_card import ChargeCard
from charge_ach import ChargeACH
from tokenize_card import TokenizeCard
from tokenize_ach import TokenizeACH
from charge_token import ChargeToken
from void import Void
from refund import Refund
from get_transaction import GetTransaction


class RedPay:
    def __init__(self, app, key, endpoint) -> None:
        self.app = app
        self.key = key
        self.endpoint = endpoint

    def ChargeCard(self, request):
        charge_card = ChargeCard(self.app, self.key, self.endpoint)
        return charge_card.Process(request)

    def ChargeACH(self, request):
        charge_ach = ChargeACH(self.app, self.key, self.endpoint)
        return charge_ach.Process(request)

    def TokenizeCard(self, request):
        tokenize_card = TokenizeCard(self.app, self.key, self.endpoint)
        return tokenize_card.Process(request)

    def TokenizeACH(self, request):
        tokenize_ach = TokenizeACH(self.app, self.key, self.endpoint)
        return tokenize_ach.Process(request)

    def ChargeToken(self, request):
        charge_token = ChargeToken(self.app, self.key, self.endpoint)
        return charge_token.Process(request)

    def Refund(self, request):
        refund = Refund(self.app, self.key, self.endpoint)
        return refund.Process(request)

    def Void(self, request):
        void = Void(self.app, self.key, self.endpoint)
        return void.Process(request)

    def GetTransaction(self, request):
        get_transaction = GetTransaction(self.app, self.key, self.endpoint)
        return get_transaction.Process(request)
