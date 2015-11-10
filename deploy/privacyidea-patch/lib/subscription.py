# -*- coding: utf-8 -*-
#
# (c) Cornelius Kölbel, NetKnights GmbH
#
# 2015-04-17 Cornelius Kölbel, <cornelius.koelbel@netknights.it>
#            Initial writeup
#
#
__doc__ = """This is the code for verifying the subscriptions on
the Univention Corporate Server
"""
import logging
from privacyidea.lib.token import get_tokens
from privacyidea.lib.error import TokenAdminError, ConfigAdminError
from privacyidea.lib.config import (set_privacyidea_config,
                                    get_from_config)
from privacyidea.lib.crypto import encrypt, geturandom
import binascii
import yaml
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import traceback


log = logging.getLogger(__name__)


def check_subscription(request, action):
    """
    Check if another token is allowed to be enrolled or assigned.
    It check if the total assigned tokens exceed the subscription count.
    Raises a TokenAdminError, if exceeded.
    """
    # get the number of assigned tokens
    token_count = get_tokens(assigned=True, count=True)
    subscription = get_subscription()
    subscription_count = subscription.get("subscription")

    # The subscription_count==0 means unlimited users
    if subscription_count > 10 or subscription_count == 0:
        check_signature(subscription)

    if subscription_count != 0 and token_count >= subscription_count:
            raise TokenAdminError("Subscription limit exceeded. You are only "
                                  "entitled to assign %s tokens to users" %
                                  subscription_count, id=34131)


def get_subscription():
    """
    Returns the license from the Config database
    """
    DEFAULT_SUB = """{'systemid': 'unknown',
                      'customername': 'Free for up to ten assigned tokens',
                      'subscription': 10,
                      'supportlevel': 'No Support',
                      'expires': 'never',
                      'signature': None}"""
    subscription = yaml.load(get_from_config("subscription", DEFAULT_SUB))
    return subscription


def check_signature(subscription):
    """
    Raises an Exception, if the signature does not match
    """
    public = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAz5gPkPYCAgab5nagG5G+
cUATHv/k5pNXU4z2Wc7h2BaJSJt2rspG109QNQyWqc28JwH/STzBQ8FZbxlyQ+zT
0xzrydfKBElLceFY/Jb7JtDdXarSvIFqejo2k5wW4yKWJYlIyqNQOYAnWVjQImOG
8Xu19uNxY+Fw5v5XBSgYPzt6q0AmzhD4udK8sYP7HLd+1LCa0X5H96Mef86NoPL3
W/E9n5Wel7Z621mPsx6lxgZiqLa2Bn79HMxkxkQ5muWIollss1yAKMStLkp7iISF
GW0yofQJjWecUHwBkZlawBz0lJBKDQObtUsjHB80VTnPGTcs4KYH+if8UHoR6Aug
4wIDAQAB
-----END PUBLIC KEY-----"""
    try:
        RSAkey = RSA.importKey(public)
        hashvalue = SHA256.new("%s%s%s%s%s" % (subscription.get("systemid"),
                                               subscription.get("customername"),
                                               subscription.get("subscription"),
                                               subscription.get("supportlevel"),
                                               subscription.get("expires"))).digest()
        signature = long(subscription.get("signature") or "100")
        r = RSAkey.verify(hashvalue, (signature,))
    except Exception as exx:
        log.debug(traceback.format_exc())
        raise ConfigAdminError("This is no valid subscription file. The "
                               "signature check failed.", id=132)
    if r is False:
        raise ConfigAdminError("This is no valid subscription file. Invalid "
                               "signature.", id=133)
    return True


def set_subscription(subscription):
    check_signature(subscription)
    set_privacyidea_config(key="subscription", value=yaml.dump(subscription),
                           desc="subscription on UCS")


def create_subscription_request():
    iv = geturandom(16)
    enc = encrypt("privacy IDEA", iv=iv)
    r = binascii.hexlify(enc + iv)
    return {"systemid": r}

