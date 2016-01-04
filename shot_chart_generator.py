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
import urllib2
from matplotlib.offsetbox import OffsetImage

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

# # create a joint plot
# joint_shot_chart = sns.jointplot(shot_df.LOC_X, shot_df.LOC_Y, stat_func = None, kind = 'scatter', space = 0, alpha = 0.5)
# joint_shot_chart.fig.set_size_inches(12,11)
# ax = joint_shot_chart.ax_joint
# draw_court(ax)

''' Joint Plot 2 '''
'''
# create our jointplot

# get our colormap for the main kde plot
# Note we can extract a color from cmap to use for 
# the plots that lie on the side and top axes
cmap=plt.cm.YlOrRd_r 

# n_levels sets the number of contour lines for the main kde plot
joint_shot_chart = sns.jointplot(shot_df.LOC_X, shot_df.LOC_Y, stat_func=None,
                                 kind='kde', space=0, color=cmap(0.1),
                                 cmap=cmap, n_levels=50)

joint_shot_chart.fig.set_size_inches(12,11)

# A joint plot has 3 Axes, the first one called ax_joint 
# is the one we want to draw our court onto and adjust some other settings
ax = joint_shot_chart.ax_joint
draw_court(ax)

# Adjust the axis limits and orientation of the plot in order
# to plot half court, with the hoop by the top of the plot
ax.set_xlim(-250,250)
ax.set_ylim(422.5, -47.5)

# Get rid of axis labels and tick marks
ax.set_xlabel('')
ax.set_ylabel('')
ax.tick_params(labelbottom='off', labelleft='off')
'''

'''
Joint Plot Style 3
'''
'''
# create our jointplot

cmap=plt.cm.gist_heat_r
joint_shot_chart = sns.jointplot(shot_df.LOC_X, shot_df.LOC_Y, stat_func=None,
                                 kind='hex', space=0, color=cmap(.2), cmap=cmap)

joint_shot_chart.fig.set_size_inches(12,11)

# A joint plot has 3 Axes, the first one called ax_joint 
# is the one we want to draw our court onto 
ax = joint_shot_chart.ax_joint
draw_court(ax)

# Adjust the axis limits and orientation of the plot in order
# to plot half court, with the hoop by the top of the plot
ax.set_xlim(-250,250)
ax.set_ylim(422.5, -47.5)
'''


# create a normal shot chart
sns.set_style("white")
sns.set_color_codes()
plt.figure(figsize = (12,11))
ax = draw_court()
plt.scatter(shot_df.LOC_X, shot_df.LOC_Y)



''' 
DO NOT MESS WITH THESE PARAMETERS (they're standard among all plots)
'''

plt.xlim(-250, 250)
plt.ylim(422.5, -47.5)
plt.tick_params(labelbottom = False, labelleft = False)

ax.set_title('James Harden FGA \n2014-15 Regular Season')
ax.text(-250,445, 'Data Source: stats.nba.com \nAuthor: Mohammad Saad (mohsaad.com)')

''' Draw Picture of Player '''
pic = urllib2.urlopen("http://stats.nba.com/media/players/230x185/201935.png","201935.png")
player_pic = plt.imread(pic)
img = OffsetImage(player_pic, zoom = 0.6)
img.set_offset((725,90))
ax.add_artist(img)

plt.show()

