import urllib3
import certifi
import datetime
import os
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
import musicUtils

# TODO: Clean up so that each web scrapper/music query/dataframe builder = 3 diff files

def write_to_walkup_db(data_dir='data', fname='WalkUpMusic.csv', overwrite=False, music_lookup=False):
    # Get team IDs
    teams_df = pd.read_csv('https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/core/Teams.csv')
    teams2_df = teams_df[teams_df.yearID ==
                         max(teams_df.yearID)].filter(items=['name', 'teamIDBR'])
    # Some of the shorthands don't match, so correct by hand
    teams2_df.replace(['CHW', 'KCR', 'SDP', 'SFG', 'TBR', 'WSN'],
                      ['CWS', 'KC', 'SD', 'SF', 'TB', 'WSH'])

    # Query MLB.com, each team has it's own walk up music page
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    d = []
    url_prefix = 'https://www.mlb.com/entertainment/walk-up/'
    for idx, team in teams2_df.iterrows():
        print(team)
        url = url_prefix + team['teamIDBR']
        r = http.request('GET', url)
        sleep(2)  # Waiting 2 seconds between pages allows time for data to load for whatever reason
        html_decode = r.data.decode('utf-8')
        soup = BeautifulSoup(html_decode, 'html.parser')

        # For each player, find the corresponding song title and artist
        table_rows = soup.findAll('tr')
        for jdx, row in enumerate(table_rows):
            name = None
            song_artist = None
            song_name = None
            if row.find('p', class_="player-name") is not None:
                name = row.find('p', class_="player-name").string.strip()
                if ' - ' in name:
                    name = name.split(' - ')[0]

                # HTML is inconsistently written,
                # usually span has a class but sometimes...
                if row.find('span', class_="song-artist") is not None:
                    song_artist = row.find('span', class_="song-artist").string
                    song_title = row.find('span', class_="song-title").string
                    lang = 'en'  # english unless otherwise specified

                # Song title/artist is in one tag, and that needs to be parsed
                else:
                    div = row.find('div', class_="song-name")
                    if len(div.findAll('span')) == 0:
                        continue
                        # If nothing in the span, no walk up music
                        song_artist = None
                        song_title = None
                        lang = None
                    else:
                        song_artist = div.find('span').string
                        if len(div.findAll('span')) == 2:
                            # If there are two spans with song & artist in each
                            song_title = row.findAll('span')[1].string
                            lang = row.findAll('span')[1]['lang'].lower()
                        else:
                            # If there is only one span with artist outside of span
                            div_sib = div.find('span').next_sibling
                            lang = 'en'
                            if div_sib is not None:
                                song_title = div_sib.string.strip()
                            else:
                                song_title = song_artist
                                song_artist = None

                # Finally, add player's information to a dict
                d.append({'Team_Name': team['name'],
                          'Team_ID': team['teamIDBR'],
                          'Player_Name': name,
                          'Song_Artist': song_artist,
                          'Song_Title': song_title,
                          'Language': lang,
                          'Date_Updated': datetime.datetime.today().date()})

    # Save to a .csv file (this will be the database for now until it gets to big)
    data_path = data_dir + '/' + fname
    if not os.path.isfile(data_path) or overwrite:
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        pd.DataFrame(d).to_csv(data_path, index=False)
    else:
        old_d = pd.read_csv(data_path)
        old_d.append(d).to_csv(data_path, index=False)

    return pd.DataFrame(d)
