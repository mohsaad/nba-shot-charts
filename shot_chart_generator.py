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
from matplotlib.patches import Circle, Rectangle, Arc

# drawing the court for our shot chart
def draw_court(ax = None, color = 'black', lw = 2, outer_lines = False):
	# if no axes object passed, use current
	if ax is None:
		ax = plt.gca()

	# Create the various parts of an NBA court

	# create hoop
	# diameter of hoop is 18" so radius of 9"
	# value of 7.5 in current coordinate system

	hoop = Circle((0,0), radius = 7.5, linewidth = lw, color = color, fill = False)

	# create backboard
	backboard = Rectangle((-30,-7.5), 60, -1, linewidth = lw, color = color, fill = False)

	# the paint
	# create two boxes, inner and outer
	# outer box
	outer_box = Rectangle((-80, -47.5), 160, 190, linewidth = lw, color = color, fill = False)

	# inner box
	inner_box = Rectangle((-60, -47.5), 120, 190, linewidth = lw, color = color, fill = False)

	# Create free throw top arc
	top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
	# Create free throw bottom arc
	bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
							linewidth=lw, color=color, linestyle='dashed')
	# Restricted Zone, it is an arc with 4ft radius from center of the hoop
	restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

	# Three point line
	# Create the side 3pt lines, they are 14ft long before they begin to arc
	corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
	corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
	# 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
	# I just played around with the theta values until they lined up with the 
	# threes
	three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

	# Center Court
	center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
						linewidth=lw, color=color)
	center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
						linewidth=lw, color=color)

	# List of the court elements to be plotted onto the axes
	court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
					  bottom_free_throw, restricted, corner_three_a,
					  corner_three_b, three_arc, center_outer_arc,
					  center_inner_arc]

	if outer_lines:
		# Draw the half court line, baseline and side out bound lines
		outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
								color=color, fill=False)
		court_elements.append(outer_lines)

	# Add the court elements onto the axes
	for element in court_elements:
		ax.add_patch(element)

	return ax


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

''' Putting the shot chart data together '''

sns.set_style("white")
sns.set_color_codes()
plt.figure(figsize = (12,11))
draw_court()
plt.scatter(shot_df.LOC_X, shot_df.LOC_Y)

plt.xlim(-250, 250)
plt.ylim(422.5, -47.5)
plt.tick_params(labelbottom = False, labelleft = False)
plt.show()

