# -*- coding: utf-8 -*-
#
# (c) Cornelius Kölbel, NetKnights GmbH
#
# 2017-11-13 Cornelius Kölbel <cornelius.koelbel@netknights.it>
#            We now simply use the base function of the subscription.
# 2016-02-15 Cornelius Kölbel, <cornelius.koelbel@netknights.it>
#            Add expiration date
# 2015-04-17 Cornelius Kölbel, <cornelius.koelbel@netknights.it>
#            Initial writeup
#
#
__doc__ = """This is the code for verifying the subscriptions on
the Univention Corporate Server
"""
import logging
from privacyidea.lib.subscriptions import check_subscription as check_base_subscription


log = logging.getLogger(__name__)


def check_subscription(request, action):
    """
    Check if another token is allowed to be enrolled or assigned.
    It check if the total assigned tokens exceed the subscription count.
    Raises a SubscriptionError, if exceeded.
    """
    # check the base subscription
    check_base_subscription("privacyidea", max_free_subscriptions=2)
