# Modified From: https://github.com/jesseward/discogs-oauth-example/
# Complete an OAuth request against the discogs.com API, using the discogs_client libary.
import sys
import discogs_client
from config import *
from discogs_client.exceptions import HTTPError

# TODO: If no config file create handler

# Your consumer key and consumer secret generated and provided by Discogs.
# See http://www.discogs.com/settings/developers . These credentials
# are assigned by application and remain static for the lifetime of your discogs
# application. the consumer details below were generated for the
# 'discogs-oauth-example' application.


def authenticat_music_db(user='walk-up-music', v=1.0):
    # A user-agent is required with Discogs API requests. Be sure to make your
    # user-agent unique, or you may get a bad response.
    user_agent = user + '/' + str(v)

    # instantiate our discogs_client object.
    d = discogs_client.Client(user_agent)

    # prepare the client with our API consumer data.
    d.set_consumer_key(Consumer_Key, Consumer_Secret)
    token, secret, url = d.get_authorize_url()

    # Prompt your user to "accept" the terms of your application. The application
    # will act on behalf of their discogs.com account.
    # If the user accepts, discogs displays a key to the user that is used for
    # verification. The key is required in the 2nd phase of authentication.
    print(('Please browse to the following URL {0}'.format(url)))

    accepted = 'n'
    while accepted.lower() == 'n':
        print()
        accepted = input('Have you authorized me at {0} [y/n]: '.format(url))

    # Waiting for user input. Here they must enter the verifier key that was
    # provided at the unqiue URL generated above.
    oauth_verifier = input('Verification code :')

    try:
        access_token, access_secret = d.get_access_token(oauth_verifier)
    except HTTPError:
        print('Unable to authenticate.')
        sys.exit(1)
    print(access_token)
    # fetch the identity object for the current logged in user.
    print(' Authentication complete.')

    # With an active auth token, we're able to reuse the client object and request
    # additional discogs authenticated endpoints, such as database search.
    return d

# Example Search:
# search_results = d.search('House For All', type='release',
#         artist='Blunted Dummies')
#
# print('\n== Search results for release_title=House For All ==')
# for release in search_results:
#     print('\n\t== discogs-id {id} =='.format(id=release.id))
#     print('\tArtist\t: {artist}'.format(artist=', '.join(artist.name for artist
#                                          in release.artists)))
#     print('\tTitle\t: {title}'.format(title=release.title))
#     print('\tYear\t: {year}'.format(year=release.year))
#     print('\tLabels\t: {label}'.format(label=','.join(label.name for label in
#                                         release.labels)))
#
# # You can reach into the Fetcher lib if you wish to used the wrapped requests
# # library to download an image. The following example demonstrates this.
# image = search_results[0].images[0]['uri']
# content, resp = discogsclient._fetcher.fetch(None, 'GET', image,
#                 headers={'User-agent': discogsclient.user_agent})
#
# print(' == API image request ==')
# print('    * response status      = {0}'.format(resp))
# print('    * saving image to disk = {0}'.format(image.split('/')[-1]))
#
# with open(image.split('/')[-1], 'w') as fh:
#     fh.write(content)
