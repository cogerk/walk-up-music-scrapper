import os
import sys
import pandas as pd
from webscrapper import write_to_walkup_db
from musicUtils import retrieve_music_metadata
from discogs_client import exceptions
from time import sleep

# Code to search pair player with their walk up music metadata, this does pretty good, Gets 90% of them about.
# We'll have to do the rest by hand :(

data_dir = 'data'
fname = 'WalkUpMusic_Discogs.csv'
overwrite = True

def make_db_entry(discogs_release, player, tries=0):
    if discogs_release is None:
        val = {'Team_Name': player.Team_Name,
                  'Team_ID': player.Team_ID,
                  'Player_Name': player.Player_Name,
                  'Song_Artist': player.Song_Artist,
                  'Song_Title': player.Song_Title,
                  'Release_Country': None,
                  'Discogs_Release_ID': None,
                  'Genres': None,
                  'Sub_Genres': None,
                  'Release_Year': None,
                  'Language': None,
                  'Date_Updated': player.Date_Updated}
    else:
        val = {'Team_Name': player.Team_Name,
                  'Team_ID': player.Team_ID,
                  'Player_Name': player.Player_Name,
                  'Song_Artist': player.Song_Artist,
                  'Song_Title': player.Song_Title,
                  'Release_Country': discogs_release.country,
                  'Discogs_Release_ID': discogs_release.id,
                  'Genres': discogs_release.genres,
                  'Sub_Genres': discogs_release.styles,
                  'Release_Year': discogs_release.year,
                  'Language': player.Language,
                  'Date_Updated': player.Date_Updated}
    return val


if not os.path.isfile('data/WalkUpMusic.csv'):
    write_to_walkup_db()
walkup_db = pd.read_csv('data/WalkUpMusic.csv')
d = []
tries = 0
for idx, player in walkup_db.iloc[400:753].iterrows():
    print(idx)
    print(player.Player_Name)
    discogs_release = retrieve_music_metadata(player.Song_Title,
                                               player.Song_Artist)
    try:
        entry = make_db_entry(discogs_release, player)
    except exceptions.HTTPError as err:
        print(err)
        if err.status_code == 429:
            sleep(60)
            if tries < sys.getrecursionlimit():
                tries = tries + 1
                make_db_entry(discogs_release, player)
            else:
                print('Recursion Limit Hit')
    d.append(entry)

data_path = data_dir + '/' + fname
if not os.path.isfile(data_path) or overwrite:
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    pd.DataFrame(d).to_csv(data_path, index=False)
else:
    old_d = pd.read_csv(data_path)
    old_d.append(d).to_csv(data_path, index=False)
