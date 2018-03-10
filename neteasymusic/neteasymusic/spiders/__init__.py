# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.


#!/usr/bin/env python
# -*- coding: utf-8 -*-

# coding=utf-8

import base64

from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
from cryptography.hazmat.backends import default_backend


def aes(text, sec_key):
    backend = default_backend()
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    cipher = Cipher(
        algorithms.AES(sec_key.encode('utf-8')),
        modes.CBC(b'0102030405060708'),
        backend=backend
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(text.encode('utf-8')) + encryptor.finalize()
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext



#!/usr/bin/env python
# -*- coding: utf-8 -*-

header = {
            'Referer': 'http://music.163.com/',
            'Host': 'music.163.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
comment_text = {
        'username': '13393376853',
        'password': 'wangyidafahao',
        'rememberLogin': 'true'
        }
comment_module = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
pubKey = '010001'
secKey = 16 * 'F'
comment_url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}/?csrf_token="

import os
import requests

from bs4 import BeautifulSoup

import contextlib
import codecs
import requests
import json
import hashlib
from bs4 import BeautifulSoup


#!/usr/bin/env python
# -*- coding: utf-8 -*-

RETURN_JSON = "return json data"
RETURE_HTML = "return html data"
PYTHON3 = False


@contextlib.contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass


def encode(s):
    if PYTHON3 is True:
        return codecs.encode(s,"utf-8").decode("utf-8")
    else:
        return s.encode("utf-8")


def hex(s):
    if PYTHON3 is True:
        return codecs.encode(bytes(s, encoding = "utf8"), 'hex')
    else:
        return s.encode("hex")


def md5(s):
    m = hashlib.md5()
    m.update(s.encode("utf-8"))
    return m.hexdigest()


def curl(url, headers, type = RETURN_JSON):
    try:
        s = requests.session()
        bs = BeautifulSoup(s.get(url, headers=headers).content, "html.parser")
        if type == RETURN_JSON:
            return json.loads(bs.text)
        elif type == RETURE_HTML:
            return bs
        else:
            return bs.text
    except Exception:
        raise


class Comment:

    def __init__(self):
        self.__headers = header
        # self.session = settings.Session()
        modulus = comment_module

        self.__encSecKey = self.rsaEncrypt(secKey, pubKey, modulus)

    def createParams(self, page=1):
        if page == 1:
            text = (
                '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
            )
        else:
            offset = str((page-1)*20)
            text = (
                '{rid:"", offset:"{}", total:"{}", limit:"20", '
                'csrf_token:""}'.format(offset, 'false')
            )
        nonce = '0CoJUm6Qyw8W8jud'
        nonce2 = 16 * 'F'
        encText = aes(
            aes(text, nonce).decode("utf-8"), nonce2
        )
        return encText

    def rsaEncrypt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = int(hex(text), 16)**int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def createSecretKey(self, size):
        return (
            ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size)))
        )[0:16]

    def post(self,song_id,page):
        data = {
            'params': self.createParams(page),
            'encSecKey': self.__encSecKey
        }
        url = comment_url.format(song_id)
        req = requests.post(
            url, headers=self.__headers, data=data, timeout=10
        )
        return req.json()


if __name__ == '__main__':
    pass
    # s = Comment().post('41651206', 1)

    # print s
    # with open('/Users/Xiaobaoxia/Desktop/comment.json', 'w') as f:
    #     f.write(s)
    # print s