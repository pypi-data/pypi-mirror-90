import json
from urllib.parse import urlencode

import pysodium
import requests
from base64 import b64decode
from ThreefoldLoginPkg.utils.crypto import generate_key_pair, get_ed_pk_in_curve, decrypt

from ThreefoldLoginPkg.utils.parse import parse_signed_attempt_from_url


class ThreefoldLogin:
    three_fold_api_host: str
    app_id: str
    seed_phrase: str
    redirect_url: str
    kyc_backend_url: str

    def __init__(self,
                 three_fold_api_host: str,
                 app_id: str,
                 seed_phrase: str,
                 redirect_url: str,
                 kyc_backend_url: str):
        self.kyc_backend_url = kyc_backend_url
        self.redirect_url = redirect_url
        self.seed_phrase = seed_phrase
        self.app_id = app_id
        self.three_fold_api_host = three_fold_api_host

    def generate_login_url(self, state: str, extra_params={}) -> str:
        key_pair = generate_key_pair(self.seed_phrase)
        public_key = get_ed_pk_in_curve(key_pair[0])

        params = {
            'state': state,
            'appid': self.app_id,
            'publickey': public_key,
            'redirecturl': self.redirect_url,
        }

        return '{}/?{}'.format(self.three_fold_api_host, urlencode(dict(params, **extra_params)))

    def parse_and_validate_redirect_url(self, url: str, state: str):
        data_object = parse_signed_attempt_from_url(url)
        signed_attempt, double_name, rest = (
            lambda signedAttempt, doubleName, **rest: (signedAttempt, doubleName, rest))(
            **data_object)

        user_public_key = self.get_public_key_for_double_name(double_name)

        sign_result = pysodium.crypto_sign_open(
            b64decode(signed_attempt),
            user_public_key
        )

        sign_result_dict = json.loads(sign_result.decode("utf-8"))

        if sign_result_dict['signedState'] != state:
            raise ValueError('state could not be matched')

        if sign_result_dict['doubleName'] != double_name:
            raise ValueError('The name cannot be matched.')

        if sign_result_dict['appId'] != self.app_id:
            raise ValueError('The appId cannot be matched.')

        encrypted_data = sign_result_dict['data']

        keyPair = generate_key_pair(self.seed_phrase)

        profile_data = decrypt(
            encrypted_data['ciphertext'],
            encrypted_data['nonce'],
            keyPair[1],
            user_public_key
        )

        return {
            'selectedImageId': sign_result_dict['selectedImageId'],
            'randomRoom': sign_result_dict['randomRoom'],
            'profile': json.loads(profile_data),
        }

    def get_public_key_for_double_name(self, double_name: str):
        url = '{0}/api/users/{1}'.format(self.three_fold_api_host, double_name)
        resp = requests.get(url)

        if resp.status_code != 200:
            raise ValueError('something went wrong')

        return b64decode(resp.json()['publicKey'])

    def verify_signed_email_idenfier(self, signed_email_identifier):
        url = '{0}/verification/verify-sei'.format(self.kyc_backend_url)
        resp = requests.post(url, json={'signedEmailIdentifier': signed_email_identifier})

        if resp.status_code != 200:
            raise ValueError('something went wrong')

        return resp.json()

    def is_email_verified(self, signed_email_identifier):
        try:
            return bool(self.verify_signed_email_idenfier(signed_email_identifier))
        except:
            return False
