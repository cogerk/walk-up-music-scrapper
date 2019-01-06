import sys
import string
import discogs_client
from time import sleep
from authorization import authenticate_music_db

# Authenticate so we can use the discogs music database
music_db = authenticate_music_db()


def normalize(s):
    """
    Reformat text before searching discogs (highly specialized)
    :param s: String to normalze
    :return:
    """
    s = s.lower().split(' feat')[0]
    s = s.lower().split(' ft.')[0]
    s = s.lower().split(' (with')[0]
    s = s.split('/')[0]
    s = s.replace('\'n', 'and')
    s = s.replace(' n ', ' and ')
    s = s.replace(' & ', ' and ')
    for p in string.punctuation:
        s = s.replace(p, '')
    return s.strip()


def loop_through_tracks(track_simple, r, tries=0):
    """
    Find if a given track name is on a given release found on discogs.
    :param track_simple: str, Simplified name of the track to identify
    :param r: discogs release, Release to search the tracklist of.
    :param tries: int, Attempt counter to manage discogs request limits
    :return: discog release
    """
    for t in r.tracklist:
        print(normalize(t.title))
        if track_simple in normalize(t.title) or normalize(t.title) in track_simple:
            print(r)
            print('Track Found')
            # Return the release if it matches track, else return none
            return r
    else:
        return None


def loop_through_results(track_simple, artist_simple, results, try_various=False, tries=0):
    """
    Given discog search results, determine if any results are the right artist. Then check for the track.
    :param track_simple: str, Simplified name of the track to identify
    :param artist_simple: str, Simplified name of the artist to identify
    :param results: discog release list, all search results
    :param try_various: bool, optional, specify if you want to check albums by various artists.
    :param tries: int, Attempt counter to manage discogs request limits
    :return: discog release
    """
    for r in results:  # Loop through all results
        release = None  # Init loop var
        try:
            for a in r.artists:  # Loop through all artists of given result
                a_name = normalize(a.name)
                artist_match = a_name in artist_simple or artist_simple in a_name  # Correct artist?
                # If specified , check if this release is by various artists
                if try_various:
                    various = a_name == 'various'
                else:
                    various = False
                # If correct artist, then check if track is on the release
                if artist_match or various:
                    try:
                        release = loop_through_tracks(track_simple, r)
                    # If too many requests to discogs server have been made, wait a minute for reset & try again
                    except discogs_client.exceptions.HTTPError as err:
                        print(err)
                        if err.status_code == 429:
                            sleep(60)
                            if tries < sys.getrecursionlimit():  # Check for iteration limit
                                return loop_through_tracks(track_simple, r, try_various, tries+1)
                            else:
                                print('Recursion Limit Hit')
                # Return the release if it matches artist & track, else return none
                if release is not None:
                    return release
        except Exception as  err:
            print(err)
            return None
    else:
        return None


def retrieve_music_metadata(track, artist, tries=0):
    """
    Given a track and artist, get the release from the discogs music database
    :param track: str, Name of the track to search for
    :param artist: str, Name of the artist to search for
    :param tries: int, Attempt counter to manage discogs request limits
    :return:
    """
    # Ensure that we're not searching for blanks
    print(track)
    print(artist)
    release = None
    results = None
    if isinstance(track, str) & isinstance(artist, str):
        track_simple = normalize(track)
        artist_simple = normalize(artist)
        try:
            # Search the discogs database
            results = music_db.search(track_simple + ' ' + artist_simple, type='release')
            if len(results) == 0:  # If nothing found, just search for the track name
                results = music_db.search(track, type='release')
        # If too many requests to discogs server have been made, wait a minute for reset & try again
        except discogs_client.exceptions.HTTPError as err:
            print(err)
            if err.status_code == 429:
                sleep(60)
                if tries < sys.getrecursionlimit():
                    return retrieve_music_metadata(track, artist, tries+1)
                else:
                    print('Recursion Limit Hit')
        try:
            # Check each result (album) to see if it is by correct artist and has track.
            release = loop_through_results(track_simple, artist_simple, results)
        # If too many requests to discogs server have been made, wait a minute for reset & try again
        except discogs_client.exceptions.HTTPError as err:
            print(err)
            if err.status_code == 429:
                sleep(60)
                if tries < sys.getrecursionlimit():
                    return loop_through_results(track_simple, 
                                                artist_simple, 
                                                results, 
                                                tries=tries+1)
                else:
                    print('Recursion Limit Hit')
        # If you didn't find anything, try again but search for releases by 'various' artists.
        if release is None:
            release = loop_through_results(track_simple, 
                                           artist_simple, 
                                           results, 
                                           try_various=True)
            # If nothing found, let me know
            if release is None:
                print('Nothing Found for ' + track + artist)

        return release
    else:
        print('No entry for this player')
        return None

