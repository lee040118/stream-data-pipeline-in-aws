from coinone.common import base_url, error_code
import base64
import simplejson as json
import hashlib
import hmac
import httplib2
import time
import logging

class Account:
    def __init__(self, token, key):
        self.token = token
        self.key = key
        self.default_payload = {"access_token": self.token}

    def info(self):
        return self._post('account/user_info')
    
    def chart(self, quote_currency,target_currency, interval):
        return self._post(f'chart/{quote_currency}/{target_currency}?interval={interval}')
    
    def ticker(self, quote_currency,target_currency):
        return self._post(f'ticker_new/{quote_currency}/{target_currency}')
        
    def _post(self, url, payload=None):
        def encode_payload(payload):
            payload[u'nonce'] = int(time.time()*1000)
            ret = json.dumps(payload).encode()
            return base64.b64encode(ret)

        def get_signature(encoded_payload, secret_key):
            signature = hmac.new(
                secret_key.upper().encode(), encoded_payload, hashlib.sha512)
            return signature.hexdigest()

        def get_response(url, payload, key):
            encoded_payload = encode_payload(payload)
            headers = {
                'Content-type': 'application/json',
                'X-COINONE-PAYLOAD': encoded_payload,
                'X-COINONE-SIGNATURE': get_signature(encoded_payload, key)
            }
            http = httplib2.Http()
            response, content = http.request(
                url, 'GET', headers=headers, body=encoded_payload)
            return content

        print(url)
        if payload is None:
            payload = self.default_payload
        res = get_response(base_url+url, payload, self.key)
        res = json.loads(res)
        if res['result'] == 'error':
            err = res['errorCode']
            raise Exception(int(err), error_code[err])
        return res