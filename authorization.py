# Modified From: https://github.com/jesseward/discogs-oauth-example/
# Complete an OAuth request against the discogs.com API, using the discogs_client libary.
# import sys
import discogs_client
from config import *
# from discogs_client.exceptions import HTTPError

# TODO: If no config file create handler

# Your consumer key and consumer secret generated and provided by Discogs.
# See http://www.discogs.com/settings/developers . These credentials
# are assigned by application and remain static for the lifetime of your discogs
# application. the consumer details below were generated for the
# 'discogs-oauth-example' application.


def authenticate_music_db(user='walk-up-music', v=1.0):
    # A user-agent is required with Discogs API requests. Be sure to make your
    # user-agent unique, or you may get a bad response.
    user_agent = user + '/' + str(v)

    # instantiate our discogs_client object.
    d = discogs_client.Client(user_agent)

    # prepare the client with our API consumer data.
    d.set_consumer_key(Consumer_Key, Consumer_Secret)
    d.set_token(token=access_token, secret=access_secret)

    # token, secret, url = d.get_authorize_url()
    # # Prompt your user to "accept" the terms of your application. The application
    # # will act on behalf of their discogs.com account.
    # # If the user accepts, discogs displays a key to the user that is used for
    # # verification. The key is required in the 2nd phase of authentication.
    # print(('Please browse to the following URL {0}'.format(url)))
    #
    # accepted = 'n'
    # while accepted.lower() == 'n':
    #     print()
    #     accepted = input('Have you authorized me at {0} [y/n]: '.format(url))
    #
    # # Waiting for user input. Here they must enter the verifier key that was
    # # provided at the unqiue URL generated above.
    # oauth_verifier = input('Verification code :')
    #
    # try:
    #     access_token, access_secret = d.get_access_token(oauth_verifier)
    # except HTTPError:
    #     print('Unable to authenticate.')
    #     sys.exit(1)
    # print(access_token)
    # # fetch the identity object for the current logged in user.
    # print(' Authentication complete.')

    # With an active auth token, we're able to reuse the client object and request
    # additional discogs authenticated endpoints, such as database search.
    return d
