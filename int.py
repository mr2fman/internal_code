from re import findall
from requests import post
from random import choice
from json import loads, dumps
from string import ascii_letters
from Crypto.Cipher.AES import new
from Crypto.Util.Padding import pad, unpad
from base64 import b64decode, b64encode

class Crypto:
	def __init__(self, auth):
	    self.key = bytearray(self.secret(auth), "utf-8")
	    self.iv = bytearray.fromhex('00' * 16)

	def secret(self, e):
		t, n, s = e[0:8], e[16:24]+e[0:8]+e[24:32]+e[8:16], 0
		while s < len(n):
			t = chr((ord(n[s][0]) - ord('0') + 5) % 10 + ord('0')) if n[s] >= '0' and n[s] <= '9' else chr((ord(n[s][0]) - ord('a') + 9) % 26 + ord('a'))
			n, s = self.replaceCharAt(n, s, t), s+1
		return n

	replaceCharAt = lambda self, e, t, i: e[0:t] + i + e[t + len(i):]
	encryption = lambda self, text: (
	    b64encode(new(self.key, 2, self.iv).encrypt(pad(text.encode(), 16))).decode())
	decryption = lambda self, text: (
	    unpad(new(self.key, 2, self.iv).decrypt(b64decode(text.encode())), 16).decode())

class Utils:
    android: dict[str, str] = {
        'app_name':'Main',
        'app_version':'3.0.6',
        'lang_code':'en',
        'package':'app.rbmain.a',
        'platform':'Android'}

    url: str = 'https://messengerg2c64.iranlms.ir/'

    @classmethod
    def rand_str(cls, length: int) -> str:
        return "".join([choice([*ascii_letters]) for _ in range(length)])

    @classmethod
    def get_phone(cls, inpot: str) -> str:
        phone = ''.join(findall(r'\d+', inpot))
        if not phone.startswith('98') and len(phone) == 11:
            phone = '98' + phone[1:]
        return phone

def sendReq(url: str, **kwargs) -> dict:
    while (True):
        with post(url, **kwargs) as response:
            if response.status_code != 200: continue
            return response.json()

def sendCode(phone: str, pass_key: str = None) -> dict:
    tmp_session = Utils.rand_str(32)
    enc = Crypto(tmp_session)
    data = {
        "api_version":"5",
        "tmp_session": tmp_session,
        "data_enc": enc.encryption(dumps({
            "method":"sendCode",
            "input":{
                "phone_number":Utils.get_phone(phone),
                "send_type":"Internal",
                "pass_key":pass_key},
        "client":Utils.android}))}
    return loads(enc.decryption(sendReq(Utils.url, json=data).get('data_enc')))


phone_number = "09150000000"
password = None

print(sendCode(phone_number, pass_key=password))
