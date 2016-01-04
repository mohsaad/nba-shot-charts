#!/usr/bin/env python
# Mohammad Saad
# 1/4/2016
# player_id.py
# Builds up a dictionary of players and their stats.nba.com IDs
# Exports to a file with a Python-loadable dictionary to be used elsewhere

import goldsberry
import pickle

player_list = goldsberry.PlayerList(AllTime = True)

player_dict = {}

# build up dictionary for every player
for i in range(0, len(player_list)):
	name = player_list[i]["PLAYERCODE"]
	if name == None:
		continue
	elif name[0] == 'H':
		name = name[8:]
	
	player_dict[name] = int(player_list[i]["PERSON_ID"])

pickle.dump(player_dict, open('player_dict.txt', 'wb'))