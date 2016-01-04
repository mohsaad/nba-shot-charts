#!/usr/bin/env python
# Mohammad Saad
# 1/4/2016
# A way to visualize shot charts and percentages
# Sourced from
# http://tinyurl.com/no8fkzp
# Original Author: Savvas Tjortjoglou

import requests
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import goldsberry


shot_chart_url = 'http://stats.nba.com/stats/shotchartdetail?CFID=33&CFPAR'\
                'AMS=2014-15&ContextFilter=&ContextMeasure=FGA&DateFrom=&D'\
                'ateTo=&GameID=&GameSegment=&LastNGames=0&LeagueID=00&Loca'\
                'tion=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&'\
                'PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=201935&Plu'\
                'sMinus=N&Position=&Rank=N&RookieYear=&Season=2014-15&Seas'\
                'onSegment=&SeasonType=Regular+Season&TeamID=0&VsConferenc'\
                'e=&VsDivision=&mode=Advanced&showDetails=0&showShots=1&sh'\
                'owZones=0'


# get webpage containing data
response = requests.get(shot_chart_url)

# grab headers to be used as column headers for dataframe
headers = response.json()['resultSets'][0]['headers']

# get shot chart data
shots = response.json()['resultSets'][0]['rowSet']

# create a Pandas dataframe
shot_df = pd.DataFrame(shots, columns = headers)

