from abc import ABC, abstractmethod
import json
import datetime
import pytz


class DataNormalizer(ABC):
    def get_header(self):
        return 'sport,event_time,home_team,away_team,home_win,away_win,booky,updated'

    @abstractmethod
    def normalize_data(self, infile_stream):
        """Trys all the data sources and returns a generator in csv of
        SPORT, EVENT_TIME, HOME-TEAM, AWAY-TEAM, HOME-WIN, AWAY-WIN, BOOKY, UPDATED
        """
        pass


class OddsAPIData(DataNormalizer):
    # Uses stats from https://the-odds-api.com/
    def __init__(self):
        self.data = None
        self.utc = pytz.timezone('UTC')

    def normalize_data(self, infile_stream):
        if not self.data:
            self.data = json.load(infile_stream)
        csv = []
        csv.append(self.get_header())
        self.data = self.data['data']
        for game in self.data:
            sport = game['sport_key']
            home_index, away_index = self.get_team_indices(game['teams'], game['home_team'])
            home, away = game['teams'][home_index], game['teams'][away_index]
            kick_off = datetime.datetime.fromtimestamp(game['commence_time'], self.utc)
            for booky in game['sites']:
                site = booky['site_key']
                home_win = 1/booky['odds']['h2h'][home_index]*100
                away_win = 1/booky['odds']['h2h'][away_index]*100
                updated = datetime.datetime.fromtimestamp(booky['last_update'], self.utc)
                csv.append([sport, str(kick_off), home, away, home_win, away_win, site, str(updated)])
        return csv

    def get_team_indices(self, teams, home_team):
        for index, team in enumerate(teams):
            if team == home_team:
                home = index
            else:
                away = index
        return home, away




DATA_SOURCES = (OddsAPIData,)


def get_normed_data(infile_stream):
    for src in DATA_SOURCES:
        try:
            infile_stream.seek(0)
            return src().normalize_data(infile_stream)
        except Exception as e:
            print(e)
            pass
    else:
        print('Didn\'t parse')
        return None
