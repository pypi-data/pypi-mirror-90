![logo](https://redshepherdmedia.s3-us-west-2.amazonaws.com/red_logo_64.png "logo")

# Red Shepherd Python API Docs

## _Follow these steps for Simple API Integration_

---

### Step 1 a- Adding the payment library using pip

> **_Add the payment library to your code using pip_**

```python
> pip install redpay
```

---

### Step 1 b - Create a RedPay object for secure API methods

> **_Create a Redpay API object which lets you access all the payment functions_**

```python
from redpay import RedPay

### REPLACE app, url and key with your PROD keys and use a valid account
### These are DEMO Keys which you can safely use for testing
app = "DEMO";
endpoint = "https://redpaystable.azurewebsites.net/";
key = "MIIBojANBgkqhkiG9w0BAQEFAAOCAY8AMIIBigKCAYEAtsQxNp3vmKVNYIxfWSi0LIRgCnPaMn0MUNouxgrs4zmg4cnvSeQ3I8YP03YbpXuWA80RvOw/nWErYAKomniJw8Y+xexMfBQ5sgJgewn3ZnRPNM9Y4Z62gwfIlsrs7Bwvpz9uUtLgeQLl1ffNaumnu1IBrqRps0EZ1QyDuu41UckTyo31C40Wez6IbeMfZeusrmPlIWqyBacdviJ5zHCA3zHNq86QMnB8HOP1U81HOSs6GTTelhD7lCoJ+fHKHxcz0MDr37fNpKpC57B0/20wBXFp9tlVtSkHcIty1lyNk2/HDH8knCdqkZk+fCvWgGwdex41x8/rM+LKC13c5J/yG6Gb2PnKhwNk4lvvnz73YAdqTUJ7qNrdtWVnOTWfbMBiNlpBCVqt8xY8UK6u83AVWrWXse0xe2Pn/kRqlXmxWT0mGEoCavjvZ9lQUL7LXAXZ1dff9r+oFUZo6xDQ3ER/OTIKa4jpvaI9S/J1drsrI1f9kkMWFwEh48dCPYplGSxzAgMBAAE=";

### Use this redpay object for all the API calls
red_pay = RedPay(app, key, endpoint)

```

---

### Step 2 a - Charge a Credit / Debit Card

```python
import json

request = {
    "account": "4111111111111111",
    "amount": 2000,
    "expmmyyyy": "122024",
    "cvv": "123",
    "accountHolder": "Anna Conda",
    "zipCode": "10001"
}

print("CHARGE Credit Card request >>>")
print(json.dumps(request, indent=2))

response = red_pay.ChargeCard(request)

print("CHARGE Credit Card response >>>")
print(json.dumps(response, indent=2))
```

**_ChargeCard Request Example_**

```python
req = {
  "account": "4111111111111111",
  "amount": 2000,
  "expmmyyyy": "122023",
  "cvv": "123",
  "cardHolderName": "Anna Conda",
  "avsZip": "10001",
};
```

**_ChargeCard Response_**

```python
{
  "responseCode": "A",
  "transactionId": "DEMO.j1kbwwwh531ivcsh",
  "authCode": "PPS531",
  "token": "9418594164541111",
  "cardLevel": "Q",
  "cardBrand": "V",
  "cardType": "C",
  "processorCode": "CC",
  "app": "DEMO",
  "account": "9418594164541111",
  "cardHolderName": "Anna Conda",
  "amount": 2000,
  "timeStamp": "12/10/2020 1:46:47 AM",
  "text": "Approval Approval",
  "ipAddress": "198.54.106.248:51554",
  "avsCode": "Z"
}
```

---

### Step 2 b - For ACH Payments

```python
import json

request = {
    "account": "1234567890",
    "routing": "121122676",
    "amount": 1200,
    "accountHolder": "Anna Conda",
}

print("CHARGE ACH request >>>")
print(json.dumps(request, indent=2))

response = red_pay.ChargeACH(request)

print("CHARGE ACH response >>>")
print(json.dumps(response, indent=2))

```

**_ChargeACH Request Example_**

```python
req = {
  "account": "1234567890",
  "accountType": "C",
  "routing": "121122676",
  "amount": 2100,
  "cardHolderName": "Anna Conda",
};
```

**_ChargeACH Response_**

```python
{
  "responseCode": "A",
  "transactionId": "DEMO.b4gxvbwexynb8u3i",
  "authCode": "SRZ79B",
  "token": "9120988649567890",
  "cardLevel": null,
  "cardBrand": null,
  "cardType": null,
  "processorCode": "CC",
  "app": "DEMO",
  "account": "9120988649567890",
  "cardHolderName": null,
  "amount": 2100,
  "timeStamp": "12/10/2020 2:06:35 AM",
  "text": "Success Success",
  "ipAddress": "198.54.106.248:56473",
  "avsCode": "U"
}
```

---

### Step 3 - Important notes

> **_IMPORTANT NOTE ||| API Amount is in cents ie 20.00 = 2000, 21.56 = 2156_**

> **_Contact us for your Production API payment keys_**
> Email us [support@redshepherd.com](mailto:support@redshepherd.com) or go to [https://dashboard.redshepherd.com/signup](https://dashboard.redshepherd.com/signup)

---

---

---

## _Other API Functions_

---

### Get a Transaction

> **_Retrieve existing Transaction from the API_**

```python
import json

request = {
    "transactionId": "DEMO.3bhjh6o8lle97cvs"
}

print("GET TRANSACTION request >>>")
print(json.dumps(request, indent=2))

response = red_pay.GetTransaction(request)

print("GET TRANSACTION response >>>")
print(json.dumps(response, indent=2))

```

**_GetTransaction Request Example_**

```python
req = {
  "transactionId": "DEMO.v9xnqezrwabwl1h7",
};
```

**_GetTransaction Response_**

```python
{
  "transactionId": "DEMO.v9xnqezrwabwl1h7",
  "app": "DEMO",
  "requestAmount": 1200,
  "responseAmount": 1200,
  "isVoided": false,
  "isRefunded": false,
  "responseCode": "A",
  "userid": "STABLE",
  "timestamp": "2020-12-24T21:28:07.841Z",
  "ipaddress": "198.54.106.248:54568",
  "processor": "CC"
}
```

---

### Tokenize a Credit / Debit Card

> **_Tokenize a card with us and process future payments just using the token, this is useful in saving Customer's payment information with us securely and using it to charge their account for future orders, Save the token securely on your side and tie it to the Customer's payment profile. DO NOT make this token public / visible anywhere on your UI or App_**

```python
import json

request = {
    "account": "4111111111111111",
    "expmmyyyy": "122024",
    "cvv": "123",
    "accountHolder": "Anna Conda",
    "zipCode": "10001"
}

print("TOKENIZE Credit Card request >>>")
print(json.dumps(request, indent=2))

response = red_pay.TokenizeCard(request)

print("TOKENIZE Credit Card response >>>")
print(json.dumps(response, indent=2))
```

**_TokenizeCard Request Example_**

```python
req = {
  "account": "4111111111111111",
  "expmmyyyy": "122023",
  "cvv": "123",
  "cardHolderName": "Anna Conda",
  "avsZip": "10001",
};
```

**_TokenizeCard Response_**

```python
{
  "responseCode": "A",
  "transactionId": "DEMO.ictm5y9ppew6rk5r",
  "authCode": "PPS405",
  "token": "9418594164541111",
  "cardLevel": "Q",
  "cardBrand": "V",
  "cardType": "C",
  "processorCode": "CC",
  "app": "DEMO",
  "account": "9418594164541111",
  "cardHolderName": "Anna Conda",
  "amount": 2000,
  "timeStamp": "12/10/2020 7:09:01 PM",
  "text": "Approval Approval",
  "ipAddress": "172.58.140.121:38164",
  "avsCode": "Z"
}
```

---

### Tokenize ACH Bank Account

> **_Tokenize a Customer's ACH Account with us and process future payments just using the token, Save the token securely on your side and tie it to the Customer's payment profile. DO NOT make this token public / visible anywhere on your UI or App_**

```python
import json

request = {
    "account": "1234567890",
    "routing": "121122676",
    "accountHolder": "Anna Conda",
}

print("TOKENIZE ACH request >>>")
print(json.dumps(request, indent=2))

response = red_pay.TokenizeACH(request)

print("TOKENIZE ACH response >>>")
print(json.dumps(response, indent=2))
```

**_TokenizeACH Request Example_**

```python
req = {
  "account": "1234567890",
  "accountType": "C",
  "routing": "121122676",
  "cardHolderName": "Anna Conda",
};
```

**_TokenizeACH Response_**

```python
{
  "responseCode": "A",
  "token": "9hcuqcrw5kg6g2o4",
  "app": "DEMO",
  "account": "7890",
  "cardHolderName": "Anna Conda",
  "amount": 0,
  "timeStamp": "12/10/2020 7:03:46 PM",
  "text": "APPROVED",
  "ipAddress": "172.58.140.121:51983"
}
```

---

### Charge a Token

> **_Charge an existing token by passing in the token and the amount_**

```python
import json

request = {
    "token": "fojid27g24u57zp1",
    "amount": 1400
}

print("CHARGE TOKEN request >>>")
print(json.dumps(request, indent=2))

response = red_pay.ChargeToken(request)

print("CHARGE TOKEN response >>>")
print(json.dumps(response, indent=2))
```

**_ChargeToken Request Example_**

```python
{
  "token": "9hcuqcrw5kg6g2o4",
  "amount": 2200
}
```

**_ChargeToken Response_**

```python
{
  "responseCode": "A",
  "transactionId": "DEMO.p97sw7y55qive1ub",
  "authCode": "2F5F9B",
  "token": "9120988649567890",
  "processorCode": "CC",
  "app": "DEMO",
  "account": "9120988649567890",
  "amount": 2200,
  "timeStamp": "12/10/2020 7:12:30 PM",
  "text": "Success Success",
  "ipAddress": "172.58.140.121:61468",
  "avsCode": "U"
}
```

---

### Void a Transaction

> **_Voiding a transaction will cancel an existing unsettled transaction, transactions normally settle in 24 hours so you should use Void function to refund the customer his money if the transaction occured in the last 24 hours, ACH Transactions might take longer to settle and voiding an ACH transaction will depend on the settlement period for that particular ACH._**
>
> > A good rule of thumb is that if you did not actually see the deposit from that transaction in your merchant bank account that means that the transaction is still not settled and can be voided.

```python
import json

request = {
    "transactionId": "DEMO.gu377jz1r98e5zfc"
}

print("VOID request >>>")
print(json.dumps(request, indent=2))

response = red_pay.Void(request)

print("VOID response >>>")
print(json.dumps(response, indent=2))
```

**_Void Request Example_**

```python
req = {
  "transactionId": "DEMO.b4gxvbwexynb8u3i",
};
```

**_Void Response_**

```python
{
  "responseCode": "A",
  "transactionId": "DEMO.ictm5y9ppew6rk5r",
  "processorCode": "CC",
  "app": "DEMO",
  "amount": 2000,
  "timeStamp": "12/10/2020 7:16:09 PM",
  "text": "Approval Approval",
  "ipAddress": "172.58.140.121:65012"
}
```

---

### Refund a Transaction

> **_Refunding a transaction will cancel an existing settled transaction, transactions normally settle in 24 hours so you should use Refund function to refund the customer his money if the transaction occured more than a day in the past. I.e. the transaction has settled and you have already received the money in your merchant bank account._**

```python
import json

request = {
    "transactionId": "DEMO.gu377jz1r98e5zfc"
}

print("REFUND request >>>")
print(json.dumps(request, indent=2))

response = red_pay.Refund(request)

print("REFUND response >>>")
print(json.dumps(response, indent=2))
```

**_Refund Request Example_**

```python
req = {
  "transactionId": "DEMO.b4gxvbwexynb8u3i",
};
```

**_Refund Response_**

```python
{
  "responseCode": "A",
  "transactionId": "DEMO.b4gxvbwexynb8u3i",
  "processorCode": "CC",
  "app": "DEMO",
  "amount": 2000,
  "timeStamp": "12/10/2020 7:16:09 PM",
  "text": "Approval Approval",
  "ipAddress": "172.58.140.121:65012"
}
```

---

> © Copyright 2020 Red Shepherd Inc.
