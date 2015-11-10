import sys
sys.stdout = sys.stderr
from privacyidea.app import create_app
from privacyidea.api.subscription import subscription_blueprint
# Now we can select the config file:
application = create_app(config_name="production", config_file="/etc/privacyidea/pi.cfg")
# For UCS we need to add the license controller
application.register_blueprint(subscription_blueprint, url_prefix='/subscription')

