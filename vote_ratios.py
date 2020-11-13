#!/usr/bin/python3

import pandas as pd
import requests
import sys
from ast import literal_eval
from collections import OrderedDict
from typing import List, Dict, Optional, OrderedDict as OrderedDictType, Any


STATES = [
    'Alaska', 'Alabama', 'Arkansas', 'Arizona', 'California', 'Colorado',
    'Connecticut', 'Delaware', 'Florida', 'Georgia',
    'Hawaii', 'Iowa', 'Idaho', 'Illinois', 'Indiana', 'Kansas', 'Kentucky',
    'Louisiana', 'Massachusetts', 'Maryland', 'Maine', 'Michigan',
    'Minnesota', 'Missouri', 'Mississippi', 'Montana', 'North Carolina',
    'North Dakota', 'Nebraska', 'New Hampshire', 'New Jersey', 'New Mexico',
    'Nevada', 'New York', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
    'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas',
    'Utah', 'Virginia', 'Vermont', 'Washington', 'Wisconsin',
    'West Virginia', 'Wyoming',
]


class Candidate:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.candidate_id = ''
        self.candidate_key = ''
        self.first_name = ''
        self.last_name = ''
        self.order = 0
        self.name_display = ''
        self.party_id = ''
        self.incumbent = 0
        self.runoff = 0
        self.winner = 0
        self.result_source = ''
        self.votes = 0
        self.percent = 0.0
        self.percent_display = ''
        self.electoral_votes = 0
        self.absentee_votes = 0
        self.absentee_percent = 0.0
        self.img_url = ''
        self.has_image = 0
        self.link = ''
        self.pronoun = ''

        self.__dict__.update(data)


class CandidateList:
    def __init__(self, data: List[Dict[str, Any]]) -> None:
        self.data = [Candidate(_) for _ in data]

    def __getitem__(self, item: int) -> Candidate:
        return self.data[item]


class CountyResult:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.trumpd = 0
        self.binenj = 0
        self.jorgensenj = 0
        self.venturaj = 0
        self.blankenshipd = 0
        self.pierceb = 0
        self.de_la_fuenter = 0
        self.write_ins: int = data.get('write-ins', 0)

        if 'write-ins' in data:
            del data['write-ins']

        self.__dict__.update(data)


class County:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.fips = ''
        self.name = ''
        self.votes = 0
        self.absentee_votes = 0
        self.reporting = 0
        self.precincts = 0
        self.absentee_method = ''
        self.eevp = 0
        self.tot_exp_vote = 0
        self.eevp_value = ''
        self.eevp_display = ''
        self.eevp_source = ''
        self.turnout_stage = 0
        self.absentee_count_progress = ''
        self.absentee_outstanding = None
        self.absentee_max_ballots = 0
        self.provisional_outstanding = None
        self.provisional_count_progress = None
        # self.results = {}
        # self.results_absentee = {}
        self.last_updated = ''
        self.leader_margin_value = 0.0
        self.leader_margin_display = ''
        self.leader_margin_name_display = ''
        self.leader_party_id = ''
        self.margin2020 = 0.0

        self.__dict__.update(data)

        self.results = CountyResult(data['results'])
        self.results_absentee = CountyResult(data['results_absentee'])


class CountyList:
    def __init__(self, data: List[Dict[str, Any]]) -> None:
        self.data = [County(_) for _ in data]

    def __getitem__(self, item: int) -> County:
        return self.data[item]


class VoteShares:
    def __init__(self, data: Dict[str, float]) -> None:
        # cumulative votes ratios for a given time series point
        # only to 3 significant figures
        # not enough to calculate D/R ratios per batch
        self.trumpd = 0.0
        self.bidenj = 0.0

        self.__dict__.update(data)

        # if you add some noise to the data beyond the 3 significant digits
        # you will see that the charts become completely scattered
        # this indicates that there are not enough significant digits to
        # accurately calculate the D/R vote ratios per batch

        # import random
        # def _random():
        #     return random.randint(-5, 5) / 10000
        #
        # self.trumpd += _random()
        # self.bidenj += _random()


class TimeSeries:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.votes = 0
        self.eevp = 0
        self.eevp_source = ''
        self.timestamp = ''

        self.__dict__.update(data)
        self.vote_shares = VoteShares(data['vote_shares'])


class TimeSeriesList:
    def __init__(self, data: List[Dict[str, Any]]) -> None:
        self.data = [TimeSeries(_) for _ in data]

    def __getitem__(self, item: int) -> TimeSeries:
        return self.data[item]


class Race:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.race_id = ''
        self.race_slug = ''
        self.url = ''
        self.state_page_url = ''
        self.ap_polls_page = ''
        self.race_type = ''
        self.election_type = ''
        self.election_date = ''
        self.runoff = 0
        self.race_name = ''
        self.office = ''
        self.officeid = ''
        self.race_rating = ''
        self.seat = ''
        self.seat_name = ''
        self.state_id = ''
        self.state_slug = ''
        self.state_name = ''
        self.state_nyt_abbrev = ''
        self.state_shape = ''
        self.state_aspect_ratio = 0
        self.party_id = ''
        self.uncontested = 0
        self.report = 0
        self.result = ''
        self.result_source = ''
        self.gain = 0
        self.lost_seat = ''
        self.votes = 0
        self.electoral_votes = 0
        self.absentee_votes = 0
        self.absentee_counties = 0
        self.absentee_count_progress = ''
        self.absentee_outstanding = None
        self.absentee_max_ballots = None
        self.provisional_outstanding = None
        self.provisional_count_progress = None
        self.poll_display = ''
        self.poll_countdown_display = ''
        self.poll_waiting_display = ''
        self.poll_time = ''
        self.poll_time_short = ''
        self.precincts_reporting = 0
        self.precincts_total = 0
        self.reporting_display = ''
        self.reporting_value = ''
        self.eevp = 0
        self.tot_exp_vote = 0
        self.eevp_source = ''
        self.eevp_value = ''
        self.eevp_display = ''
        self.county_data_source = ''
        self.incumbent_party = ''
        self.no_forecast = 0
        self.last_updated = ''
        # self.candidates = []
        self.has_incumbent = 0
        self.leader_margin_value = 0.0
        self.leader_margin_votes = 0
        self.leader_margin_display = ''
        self.leader_margin_name_display = ''
        self.leader_party_id = ''
        # self.counties = []
        self.votes2016 = 0
        self.margin2016 = 0.0
        self.clinton2016 = 0
        self.trump2016 = 0
        self.votes2012 = 0
        self.margin2012 = 0.0
        self.expectations_text = ''
        self.expectations_text_short = ''
        self.absentee_ballot_deadline = 0
        self.absentee_postmark_deadline = 0
        self.update_sentences = {}
        self.race_diff = {}
        self.winnerCalledTimestamp = 0
        # self.timeseries = []

        self.__dict__.update(data)

        self.candidates = CandidateList(data['candidates'])
        self.counties = CountyList(data['counties'])
        self.timeseries = TimeSeriesList(data['timeseries'])


class RaceList:
    def __init__(self, data: List[Dict[str, Any]]) -> None:
        self.data: List[Race] = [Race(_) for _ in data]

    def __getitem__(self, item: int) -> Race:
        return self.data[item]


class PartyControl:
    """
    I never used this.
    """
    def __init__(self, data: Any) -> None:
        self.data = data

    def __getitem__(self, item: int) -> Any:
        return self.data[item]


class LiveUpdates:
    """
    I never used this.
    """
    def __init__(self, data: Any) -> None:
        self.data = data

    def __getitem__(self, item: int) -> Any:
        return self.data[item]


class Data:
    """
    The data class held by the StateResults class.
    """
    def __init__(self, data: Dict[str, Any]) -> None:
        self.races = RaceList(data['races'])
        self.party_control = PartyControl(data['party_control'])
        self.liveUpdates = PartyControl(data['liveUpdates'])


class Meta:
    """
    I never used this.
    """
    def __init__(self, data: Dict) -> None:
        self.__dict__.update(data)


class PostProcessData:
    """
    This is where all the data is stored for the csv file and for the plots.
    It is held by the StateResults class and the AllResults class.
    This is where the D/R ratios are calculated.
    """
    def __init__(self) -> None:
        self.votes: List[int] = []
        self.eevp: List[int] = []
        self.eevp_source: List[str] = []
        self.timestamp: List[str] = []
        self.state: List[str] = []
        self.expected_votes: List[int] = []
        self.trump2016: List[int] = []
        self.votes2012: List[int] = []
        self.votes2016: List[int] = []
        self.vote_share_rep: List[float] = []
        self.vote_share_dem: List[float] = []
        self.vote_share_trd: List[float] = []
        # new columns that I added
        self.delta_votes: List[int] = []
        self.total_rep_votes: List[float] = []
        self.total_dem_votes: List[float] = []
        self.delta_rep: List[float] = []
        self.delta_dem: List[float] = []
        self.delta_rep_share: List[float] = []
        self.delta_dem_share: List[float] = []
        self.timestamp_alt: List[str] = []
        self.dem_over_rep: List[float] = []

    def copy(self) -> 'PostProcessData':
        cpy = PostProcessData()
        for key, item in self.__dict__.items():
            getattr(cpy, key).extend(item)
        return cpy

    def extend(self, other: 'PostProcessData') -> None:
        for key, item in other.__dict__.items():
            getattr(self, key).extend(item)

    def clear(self) -> None:
        for item in self.__dict__.values():
            item.clear()

    def update(self, sr: 'StateResults') -> None:
        """
        Update the data for the state results.  D/R ratioes are calculated by this function.
        """
        self.clear()

        presidential_race = sr.data.races[0]  # first index is the presidential race
        timeseries = presidential_race.timeseries
        state_name = presidential_race.state_name

        for ts in timeseries.data:
            self.votes.append(ts.votes)
            self.eevp.append(ts.eevp)
            self.eevp_source.append(ts.eevp_source)
            self.timestamp.append(ts.timestamp)
            self.state.append(state_name)
            self.expected_votes.append(presidential_race.tot_exp_vote)
            self.trump2016.append(presidential_race.trump2016)
            self.votes2012.append(presidential_race.votes2012)
            self.votes2016.append(presidential_race.votes2016)
            self.vote_share_rep.append(ts.vote_shares.trumpd)
            self.vote_share_dem.append(ts.vote_shares.bidenj)
            self.vote_share_trd.append(1.0 - ts.vote_shares.trumpd - ts.vote_shares.bidenj)
            self.total_rep_votes.append(self.votes[-1] * self.vote_share_rep[-1])  # total rep votes, running total
            self.total_dem_votes.append(self.votes[-1] * self.vote_share_dem[-1])  # total dem votes, running total

            if len(self.votes) == 1:
                # there are no deltas to be calculated, yet
                self.delta_votes.append(0)
                self.delta_rep.append(0)
                self.delta_dem.append(0)
                self.delta_rep_share.append(0)
                self.delta_dem_share.append(0)
            else:
                self.delta_votes.append(self.votes[-1] - self.votes[-2])  # total votes for current batch
                self.delta_rep.append(self.total_rep_votes[-1] - self.total_rep_votes[-2])  # number of rep votes for current batch
                self.delta_dem.append(self.total_dem_votes[-1] - self.total_dem_votes[-2])  # number of dem votes for current batch

                if self.delta_votes[-1] != 0:
                    self.delta_rep_share.append(self.delta_rep[-1] / self.delta_votes[-1])  # share of rep votes for current batch
                    self.delta_dem_share.append(self.delta_dem[-1] / self.delta_votes[-1])  # share of dem votes for current batch
                else:
                    # can't divide by zero
                    self.delta_rep_share.append(0)
                    self.delta_dem_share.append(0)

            try:
                # D/R ratio for the current batch
                # see comments starting on line 122 to see why this calculation is NOT accurate
                self.dem_over_rep.append(self.delta_dem_share[-1] / self.delta_rep_share[-1])
            except ZeroDivisionError:
                # can't divide by zero
                self.dem_over_rep.append(0.0)

            # ended up not using timestamp_alt, but it's handy if you want a valid datetime format
            self.timestamp_alt.append(self.timestamp[-1].replace('T', ' ').replace('Z', ''))


class StateResults:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = Data(data['data'])
        self.meta = Meta(data['meta'])

        ##############################
        self.post_process_data = PostProcessData()

    def update(self) -> None:
        self.post_process_data.clear()
        self.post_process_data.update(self)

    def save_plot(self, filename: str, title: str) -> None:
        """
        Saves D/R Ratio plot to a png file.  Not a pretty plot, but it works.
        """
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.set_ylim(0.0, 2.0)
        ax.plot(
            [i for i in range(len(self.post_process_data.dem_over_rep))], # x axis
            self.post_process_data.dem_over_rep, # y axis
            'o'
        )
        ax.set(xlabel='Batch Number', ylabel='D/R Vote Ratio of Batch', title=title)
        ax.grid()
        fig.savefig(filename)
        plt.close()


class AllResults:
    def __init__(self) -> None:
        self.data: OrderedDictType[str, StateResults] = OrderedDict()

        ##########################
        self.post_process_data = PostProcessData()

    def load_data(self, download: bool = True) -> None:
        """
        Load all state results data.  If download is True, then the data will be downloaded.
        Otherwise, it is assumed to have already been downloaded.
        """
        if download:
            self._download_data()

        all_results = OrderedDict()

        for state in STATES:
            print(f'Loading {state}')
            formatted_state = state.lower().replace(' ', '-')

            with open(f'data/{formatted_state}_data.json') as f:
                state_results = literal_eval(f.read())

            all_results[formatted_state] = StateResults(state_results)

        self.data.clear()
        self.data.update(all_results)

    def _download_data(self) -> None:
        """
        Download the state results data.
        """
        import os
        if not os.path.exists('data'):
            os.mkdir('data')
        for state in STATES:
            print(f'Downloading {state}')
            formatted_state = state.lower().replace(' ', '-')
            state_results = requests.get(
                'https://static01.nyt.com/elections-assets/2020/data/api/2020-11-03/race-page/{}/president.json'.format(
                    formatted_state)).json()
            with open(f'data/{formatted_state}_data.json', 'w') as f:
                f.write(str(state_results))

    def update(self) -> None:
        """
        Update all state results data and save plots.
        """
        self.post_process_data.clear()
        for key, item in self.data.items():
            item.update()
            self.post_process_data.extend(item.post_process_data)
            item.save_plot(f"{key.replace(' ', '_')}.png", key)

    def to_csv(self, filename: str) -> None:
        """
        Save all state results data to csv file.
        """
        import pandas as pd
        df = pd.DataFrame(self.post_process_data.__dict__)
        df.to_csv(filename, encoding='utf-8')


def _print_dct_items(data: Dict[str, Any]) -> None:
    """
    I used this function to help create the classes for all of the dicts in the json data.
    """
    for key, item in data.items():
        if isinstance(item, str):
            i = f"self.{key} = ''"
        elif isinstance(item, int):
            i = f'self.{key} = 0'
        elif isinstance(item, float):
            i = f'self.{key} = 0.0'
        elif isinstance(item, bool):
            i = f'self.{key} = False'
        elif isinstance(item, dict):
            i = f'self.{key} = {{}}'
        elif isinstance(item, list):
            i = f'self.{key} = []'
        elif isinstance(item, type(None)):
            i = f'self.{key} = None'
        else:
            raise Exception(type(item))

        print(i)


if __name__ == '__main__':
    # D/R ratio per batch is calculated on line 390
    # see comments starting on line 122 for comments on why the D/R ratio calculation is NOT accurate
    data = AllResults()
    data.load_data(download=False)  # set download=True to download data if you haven't already
    data.update()
    data.to_csv('vote_ratios.csv')