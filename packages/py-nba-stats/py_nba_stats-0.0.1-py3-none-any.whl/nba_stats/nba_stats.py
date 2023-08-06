import requests
from datetime import datetime
import re
from dataclasses import dataclass, field
from bs4 import BeautifulSoup
from constant import (
    SeasonAvgTableOffset,
    GameTableOffset,
    TEAM_INFO_URL,
    GAME_LOG_URL,
    PLAYER_INFO_URL,
    PLAYER_LU_TABLE
)

@dataclass
class DataAttribute:
    names: list = field(default_factory=list)
    num_game: int = 1
    fg_made: float = 0.0
    fg_attempt: float = 0.0
    three_made: float = 0.0
    three_attempt: float = 0.0
    ft_made: float = 0.0
    ft_attempt: float = 0.0
    rebound: float = 0.0
    assist: float = 0.0
    turnover: float = 0.0
    steal: float = 0.0
    block: float = 0.0
    point: float = 0.0

    @classmethod
    def create_data(cls, name, table, index, per_game=True):
        if per_game:
            offsets = GameTableOffset()
            num_game = 1
        else:
            offsets = SeasonAvgTableOffset()
            num_game = table[index + offsets.gm_offset]
        return DataAttribute([name],
                          num_game,
                          float(table[index + offsets.fgm_offset]),
                          float(table[index + offsets.fga_offset]),
                          float(table[index + offsets.tm_offset]),
                          float(table[index + offsets.ta_offset]),
                          float(table[index + offsets.ftm_offset]),
                          float(table[index + offsets.fta_offset]),
                          float(table[index + offsets.reb_offset]),
                          float(table[index + offsets.ast_offset]),
                          float(table[index + offsets.to_offset]),
                          float(table[index + offsets.stl_offset]),
                          float(table[index + offsets.blk_offset]),
                          float(table[index + offsets.pt_offset]))

    def __add__(self, other):
        return DataAttribute(self.names + other.names, 
                             self.num_game + other.num_game, 
                             self.fg_made + other.fg_made, 
                             self.fg_attempt + other.fg_attempt, 
                             self.three_made + other.three_made, 
                             self.three_attempt + other.three_attempt, 
                             self.ft_made + other.ft_made, 
                             self.ft_attempt + other.ft_attempt, 
                             self.rebound + other.rebound, 
                             self.assist + other.assist, 
                             self.turnover + other.turnover, 
                             self.steal + other.steal, 
                             self.block + other.block, 
                             self.point + other.point)

    def __truediv__(self, factor):
        return DataAttribute(self.names, 
                             self.num_game, 
                             round(self.fg_made / factor, 2), 
                             round(self.fg_attempt / factor, 2),
                             round(self.three_made / factor, 2),
                             round(self.three_attempt / factor, 2),
                             round(self.ft_made / factor, 2),
                             round(self.ft_attempt / factor, 2),
                             round(self.rebound / factor, 2),
                             round(self.assist / factor, 2),
                             round(self.turnover / factor, 2),
                             round(self.steal / factor, 2),
                             round(self.block / factor, 2),
                             round(self.point / factor, 2))

class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        arg = args[0].title()
        if arg not in cls._instances:
            cls._instances[arg] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[arg]

class NoDataException(Exception):
    pass

class Player(metaclass=Singleton):
    """
    A class represent a player
    
    Attributes:
        name (string):                              player's full name
        player_id (int):                            player 4 digit id
        game_raw_data (BeautifulSoup object):       internal data for processing
        yearly_raw_data (BeautifulSoup object):     internal data for processing
        team (string):                              player's team
        number (int):                               player's number
        avg_pt (float):                             average point for current season
        avg_reb (float):                            average rebound for current season
        avg_ast (float):                            average assist for current season
        position (string):                          position
        college (string):                           college the player attended
        notes (list[str]):                          recent notes if there is any
    """
    def __init__(self, name):
        self.name = name.title()
        if self.name not in PLAYER_LU_TABLE:
            raise Exception(f'Do not have record for {self.name}')
        self.player_id = PLAYER_LU_TABLE[self.name]
        self._game_raw_data = {}
        self._yearly_raw_data = None
        self._team = None
        self._number = None
        self._avg_pt = None
        self._avg_reb = None
        self._avg_ast = None
        self._position = None
        self._college = None
        self._notes = None

    def __str__(self):
        return self.name

    @property
    def number(self):
        if self._number:
            return self._number
        self._number = list(self.yearly_raw_data.find(attrs={"class": "IbBox Whs(n)"}).stripped_strings)[1].strip('#')
        return self._number

    @property
    def position(self):
        if self._position:
            return self._position
        self._position = list(self.yearly_raw_data.find(attrs={"class": "IbBox Whs(n)"}).stripped_strings)[3]
        return self._position

    @property
    def avg_pt(self):
        if self._avg_pt:
            return self._avg_pt
        try:
            self._avg_pt = float(list(self.yearly_raw_data.find(attrs={"class": "ys-player-key-stats"}).stripped_strings)[1])
        except:
            self._avg_pt = 0.0
        return self._avg_pt

    @property
    def avg_reb(self):
        if self._avg_reb:
            return self._avg_reb
        try:
            self._avg_reb = float(list(self.yearly_raw_data.find(attrs={"class": "ys-player-key-stats"}).stripped_strings)[3])
        except:
            self._avg_reb = 0.0
        return self._avg_reb

    @property
    def avg_ast(self):
        if self._avg_ast:
            return self._avg_ast
        try:
            self._avg_ast = float(list(self.yearly_raw_data.find(attrs={"class": "ys-player-key-stats"}).stripped_strings)[-1])
        except:
            self._avg_ast = 0.0
        return self._avg_ast

    @property
    def team(self):
        if self._team:
            return self._team
        self._team = self.yearly_raw_data.find_all(href=re.compile("^/nba/teams/"))[0].get('title')
        return self._team

    @property
    def college(self):
        if self._college is not None:
            return self._college
        data = list(self.yearly_raw_data.find(attrs={"class": "IbBox Whs(n)"}).stripped_strings)
        if 'College' in data:
            self._college = data[data.index('College') + 2]
        else:
            self._college = ''
        return self._college

    @property
    def notes(self):
        if self._notes is not None:
            return self._notes
        data = list(self.yearly_raw_data.find(attrs={'id':'Col1-1-PlayersNotes-Proxy'}).stripped_strings)
        self._notes = []
        if not data:
            return self._notes
        for i, text in enumerate(data):
            if re.match(r'\(\d+ of \d+\)', text):
                self._notes.append(data[i + 1])
        return self._notes

    @property
    def yearly_raw_data(self):
        if self._yearly_raw_data is not None:
            return self._yearly_raw_data
        url = PLAYER_INFO_URL.format(player_id=self.player_id)
        raw_data = requests.get(url)
        if raw_data.status_code != 200:
            raise Exception(f'Error getting data from {url=}')
        self._yearly_raw_data = BeautifulSoup(raw_data.text, features="lxml")
        return self._yearly_raw_data

    def get_game_raw_data(self, year):
        if self._game_raw_data.get(year):
            return self._game_raw_data[year]
        url = GAME_LOG_URL.format(player_id=self.player_id, year=year)
        raw_data = requests.get(url)
        if raw_data.status_code != 200:
            raise Exception(f'Error getting data from {url=}')
        self._game_raw_data[year] = BeautifulSoup(raw_data.text, features="lxml")
        return self._game_raw_data[year]

    def get_yearly_data(self, year='current'):
        """
        return the yearly average represented by DataAttribute dataclass

        Required argument:
            year (int):         a 4 digit formatted year, eg, 2019. If it's "current", it'll get the current year. default=current

        Return:
            DataAttribute object
        """
        avg_table = self._get_table(game=False)
        avg_table = list(avg_table.stripped_strings)
        for index, line in enumerate(avg_table):
            if str(self._get_year(year)) in line:
                return DataAttribute.create_data(line, avg_table, index, per_game=False)
        return DataAttribute(num_game=0)

    def _get_table(self, game=True, year=None):
        try:
            if game:
                if year is None:
                    raise Exception('Year cannot be None when game is set to true')
                index = 0
                year = self._get_year(year)
                data = self.get_game_raw_data(year)
            else:
                index = 1
                data = self.yearly_raw_data
            table = data.find_all('table')
            if len(table) <= 1:
                return table[0]
            return table[index]
        except:
            raise NoDataException(f'Error getting table {game=} {index=}')
    
    def _get_year(self, year):
        if isinstance(year, str) and year.lower() == 'current':
            year = datetime.now().year
        return int(year)

    def get_recent_games_data(self, game_type='all', home_only=False, away_only=False, games=5, year='current'):
        """
        Parameters:
            game_type (string): accepted types are all, reg, or post, default=all
            home_only (bool):   home game only, default=False
            away_only (bool):   away game only, default=False
            games (int):        the number of games, default=5
            year (int):         a 4 digit formatted year, eg, 2019. If it's "current", it'll get the current year. default=current

        Return:
            a list of DataAttribute objects
        """
        if games <= 0:
            raise Exception(f'period must be a positive integer')
        res = []
        total_table = self._get_table(year=year)
        total_table = list(total_table.stripped_strings)
        for index, line in enumerate(total_table):
            if re.match(r'\d{2,3}-\d{2,3}', line):
                opponent = total_table[index - 1]
                if '@' in opponent and home_only:
                    continue
                if '@' not in opponent and away_only:
                    continue
                if game_type.lower() == 'reg' and total_table[index + 1] != 'Reg':
                    continue
                if game_type.lower() == 'post' and total_table[index + 1] != 'Post':
                    continue
                res.append(DataAttribute.create_data(opponent, total_table, index))
                games -= 1
                if games <= 0:
                    break
        return res

    def get_recent_games_avg_stats(self, game_type='all', home_only=False, away_only=False, games=5, year='current'):
        """
        Parameters:
            game_type (string): accepted types are all, reg, or post, default=all
            home_only (bool):   home game only, default=False
            away_only (bool):   away game only, default=False
            games (int):        the number of games, default=5
            year (int):         a 4 digit formatted year, eg, 2019. If it's "current", it'll get the current year. default=current

        Return:
            a list of DataAttribute objects
        """
        stats = self.get_recent_games_data(home_only, away_only, games, year)
        if not stats:
            return DataAttribute(num_game=0)
        res = stats[0]
        for s in stats[1:]:
            res += s
        return res / len(stats)

    def get_data_by_opponent(self, oppo, game_type='all', year='current'):
        """
        Parameter:
            opponent (string):  the 3 charater team name
            year (int):         a 4 digit formatted year, eg, 2019. If it's "current", it'll get the current year. default=current

        Return:
            a list of DataAttribute objects
        """
        res = []
        game_table = self._get_table(year=year)
        game_table = list(game_table.stripped_strings)
        for index, line in enumerate(game_table):
            if oppo.upper() == line or '@' + oppo.upper() == line:
                if game_type.lower() == 'reg' and game_table[index + 2] != 'Reg':
                    continue
                if game_type.lower() == 'post' and game_table[index + 2] != 'Post':
                    continue
                res.append(DataAttribute.create_data(line, game_table, index + 1))
        return res

    def get_avg_stats_by_opponent(self, oppo, game_type='all', year='current'):
        """
        Parameter:
            oppo (string):      the 3 charater team name
            game_type (string): accepted types are all, reg, or post, default=all
            year (int):         a 4 digit formatted year, eg, 2019. If it's "current", it'll get the current year. default=current
        
        Return:
            DataAttribute object
        """
        stats = self.get_data_by_opponent(oppo, year)
        if not stats:
            return DataAttribute(num_game=0)
        res = stats[0]
        for s in stats[1:]:
            res += s
        return res / len(stats)

    def clear_cache(self):
        """
        clear caches
        Parameter:
            None

        Return:
            None
        """
        self._yearly_raw_data = None
        self._game_raw_data = {}
        self._team = None
        self._number = None
        self._avg_pt = None
        self._avg_reb = None
        self._avg_ast = None
        self._position = None
        self._college = None
        self._notes = None

class Team(metaclass=Singleton):
    """
    A class represents a team

    Attributes:
        name (string):                      team name
        win (int):                          number of wins for current season
        loss (int):                         number of loss for current season
        pt (float):                         average point
        reb (float):                        average rebound
        fg (float):                         average fild goal percentage
        percent_3pt (float):                average 3 point percentage
        standing (string):                  team standing
        raw_data (BeautifulSoup object):    internal data for processing
        players (list[Player]):             list of player objects
    """

    def __init__(self, name):
        self.name = name.title()
        self._win = None
        self._loss = None
        self._pt = None
        self._reb = None
        self._fg = None
        self._percent_3pt = None
        self._standing = None
        self._raw_data = None
        self._players = None

    def __str__(self):
        return self.name

    def _convert_name(self):
        data = self.name.split()
        if len(data) == 2:
            return data[0].lower()
        if 'los angelas' in self.name.lower():
            return 'la-' + data[-1].lower()
        return f'{data[0].lower()}-{data[1].lower()}'
    
    @property
    def raw_data(self):
        if self._raw_data is not None:
            return self._raw_data
        url = TEAM_INFO_URL.format(team_name=self._convert_name())
        raw_data = requests.get(url)
        if raw_data.status_code != 200:
            raise Exception(f'Error getting data from {url=}')
        self._raw_data = BeautifulSoup(raw_data.text)
        return self._raw_data

    @property
    def win(self):
        if self._win is not None:
            return self._win
        data = list(self.raw_data.find(attrs={'class' :'IbBox Whs(n)'}).stripped_strings)[5]
        self._win = int(data.split('-')[0])
        return self._win
        
    @property
    def loss(self):
        if self._loss is not None:
            return self._loss
        data = list(self.raw_data.find(attrs={'class' :'IbBox Whs(n)'}).stripped_strings)[5]
        self._loss = int(data.split('-')[1])
        return self._loss

    @property
    def pt(self):
        if self._pt is not None:
            return self._pt
        data = list(self.raw_data.find(attrs={'class' :'IbBox Whs(n)'}).stripped_strings)
        index = data.index('PPG')
        self._pt = float(data[index - 1])
        return self._pt

    @property
    def reb(self):
        if self._reb is not None:
            return self._reb
        data = list(self.raw_data.find(attrs={'class' :'IbBox Whs(n)'}).stripped_strings)
        index = data.index('RPG')
        self._reb = float(data[index - 1])
        return self._reb

    @property
    def fg(self):
        if self._fg is not None:
            return self._fg
        data = list(self.raw_data.find(attrs={'class' :'IbBox Whs(n)'}).stripped_strings)
        index = data.index('FG%')
        self._fg = float(data[index - 1])
        return self._fg

    @property
    def percent_3pt(self):
        if self._percent_3pt is not None:
            return self._percent_3pt
        data = list(self.raw_data.find(attrs={'class' :'IbBox Whs(n)'}).stripped_strings)
        index = data.index('3P%')
        self._percent_3pt = float(data[index - 1])
        return self._percent_3pt

    @property
    def standing(self):
        if self._standing is not None:
            return self._standing
        self._standing = list(self.raw_data.find(attrs={'class' :'IbBox Whs(n)'}).stripped_strings)[3]
        return self._standing

    @property
    def players(self):
        if self._players is not None:
            return self._players
        self._players = []
        data = list(self.raw_data.find('table').stripped_strings)
        for index, item in enumerate(data):
            if re.match(r'\d+', item):
                player = data[index + 1]
                if player.title() in PLAYER_LU_TABLE:
                    self._players.append(Player(player))
        return self._players

    def clear_cache(self):
        """
        clear caches
        Parameter:
            None

        Return:
            None
        """
        self._win = None
        self._loss = None
        self._pt = None
        self._reb = None
        self._fg = None
        self._percent_3pt = None
        self._standing = None
        self._raw_data = None
        self._players = None
