# -*- coding: utf-8 -*-
#
# (c) Cornelius Kölbel, NetKnights GmbH
#
# 2015-04-14 Cornelius Kölbel, <cornelius.koelbel@netknights.it>
#            Initial writeup
#
#
__doc__ = """This is the license controller API for running privacyIDEA on
the Univention Corporate Server
"""
from flask import (Blueprint,
                   request, current_app, Response,
                   stream_with_context)
from privacyidea.api.lib.utils import (send_result)
from privacyidea.lib.subscription import (get_subscription,
                                          create_subscription_request,
                                          set_subscription)
import logging
import yaml
from privacyidea.lib.log import log_with
from privacyidea.api.auth import (user_required, admin_required)

log = logging.getLogger(__name__)

subscription_blueprint = Blueprint('subscription_blueprint', __name__)


@subscription_blueprint.route('/', methods=['GET'])
@log_with(log)
@admin_required
def api_get():
    """
    Return the subscription object as JSON.
    """
    subscription = get_subscription()
    return send_result(subscription)


@subscription_blueprint.route('/', methods=['POST'])
@log_with(log)
@admin_required
def api_set():
    """
    """
    subscription_file = request.files['file']
    file_contents = subscription_file.read()
    subscription = yaml.load(file_contents)
    set_subscription(subscription)
    return send_result(True)


@subscription_blueprint.route('/request', methods=['POST', 'GET'])
@log_with(log)
@admin_required
def api_request():
    """
    Create a subscription request.
    This request needs to be sent to NetKnights to create a subscription
    """
    subscription_request = create_subscription_request()
    return send_result(subscription_request)


