
from base64 import b64encode, b64decode
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_v1_5

import http.client
import json


class Session:
    # app - name of application
    # key - unique encryption key in base64string
    # endpoint - RedPay server endpoint
    def __init__(self, app, key, endpoint, route) -> None:
        self.app = app
        self.key = key
        self.endpoint = endpoint
        self.route = route

        # Generate and save Random key and iv using AES Cipher
        self.random_key = get_random_bytes(32)
        self.cipher = AES.new(self.random_key, AES.MODE_CBC)
        self.random_iv = b64encode(self.cipher.iv).decode()

        # Have AES decipher ready to decrypt response
        self.decipher = AES.new(self.random_key, AES.MODE_CBC, self.cipher.iv)

        # Generate random encrypted key using random_key and RSA public key
        rsa_key = RSA.import_key(b64decode(key))
        self.rsa = PKCS1_v1_5.new(rsa_key)
        self.encrypted_random_key = self.rsa.encrypt(
            b64encode(self.random_key))

        # Create session request
        data = {
            "rsaPublicKey": self.key,
            "aesKey": b64encode(self.encrypted_random_key).decode()
        }
        json_data = json.dumps(data)

        # POST Request for sessionId
        conn = http.client.HTTPSConnection(self.endpoint)
        headers = {'Content-type': 'application/json'}
        # Send the request
        conn.request('POST', self.route, json_data, headers)
        response = json.loads(conn.getresponse().read().decode())
        # Parse and set sessionId
        if "sessionId" in response:
            self.sessionId = response["sessionId"]
        else:
            self.sessionId = "ERROR Unable to get session from server"
        # print("sessionId -> " + self.sessionId)

    def Send(self, request):
        plaintext_request = json.dumps(request)
        # print("plaintext_request ->" + plaintext_request)
        encrypted = self.cipher.encrypt(
            pad(plaintext_request.encode(), AES.block_size))
        encrypted_request = b64encode(encrypted).decode()

        data = {
            "sessionId": self.sessionId,
            "app": self.app,
            "iv": self.random_iv,
            "aesData": encrypted_request
        }
        json_data = json.dumps(data)
        # print("encrypted_request ->" + json_data)

        # POST Request packet
        conn = http.client.HTTPSConnection(self.endpoint)
        headers = {'Content-type': 'application/json'}
        # Send the request
        conn.request('POST', self.route, json_data, headers)
        encrypted_response = json.loads(conn.getresponse().read().decode())
        # print("encrypted_response ->" + json.dumps(encrypted_response, indent=2))
        # print("encrypted_response aesData ->" + encrypted_response["aesData"])

        # Decrypt response
        plain_response = unpad(self.decipher.decrypt(
            b64decode(encrypted_response["aesData"])), AES.block_size).decode()
        # print("plain_response ->" + plain_response)
        return json.loads(plain_response)
