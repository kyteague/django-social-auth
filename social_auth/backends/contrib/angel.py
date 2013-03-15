"""
settings.py should include the following:

    ANGEL_CLIENT_ID = '...'
    ANGEL_CLIENT_SECRET = '...'

Optional scope to include 'email' and/or 'messages' separated by space:

    ANGEL_AUTH_EXTRA_ARGUMENTS = {'scope': 'email messages'}

More information on scope can be found at https://angel.co/api/oauth/faq
"""
from social_auth.utils import dsa_urlopen
from social_auth.backends import BaseOAuth2, OAuthBackend


ANGEL_SERVER = 'angel.co'
ANGEL_AUTHORIZATION_URL = 'https://angel.co/api/oauth/authorize/'
ANGEL_ACCESS_TOKEN_URL = 'https://angel.co/api/oauth/token/'
ANGEL_CHECK_AUTH = 'https://api.angel.co/1/me/'


class AngelBackend(OAuthBackend):
    name = 'angel'

    def get_user_id(self, details, response):
        return response['id']

    def get_user_details(self, response):
        """Return user details from Angel account"""
        username = response['angellist_url'].split('/')[-1]
        first_name = response['name'].split(' ')[0]
        last_name = response['name'].split(' ')[-1]
        email = response['email']
        return {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        }


class AngelAuth(BaseOAuth2):
    """Angel OAuth mechanism"""
    AUTHORIZATION_URL = ANGEL_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = ANGEL_ACCESS_TOKEN_URL
    AUTH_BACKEND = AngelBackend
    SETTINGS_KEY_NAME = 'ANGEL_CLIENT_ID'
    SETTINGS_SECRET_NAME = 'ANGEL_CLIENT_SECRET'
    REDIRECT_STATE = False
    STATE_PARAMETER = False

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        try:
            return dsa_urlopen(ANGEL_CHECK_AUTH, params={
                'access_token': access_token
            }).json()
        except ValueError:
            return None


# Backend definition
BACKENDS = {
    'angel': AngelAuth,
}
