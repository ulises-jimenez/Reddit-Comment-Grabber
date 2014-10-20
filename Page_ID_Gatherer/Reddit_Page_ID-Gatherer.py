import requests
import pandas as pd
import time

subreddits = ["pics", "soccer", "nba", "videos", "hiphopheads", "fitness", "running", "nintendo", 
				"cscareerquestions", "askreddit"] # list of subreddits to be used in experiment, add whichever subreddits are needed
				
timeperiod = 'day' # period to take threads from

limit = '10' # how many threads to take from each subreddit

def nested_maker(sreddits, period, resultlength): # Takes in parameters, returns a pandas DataFrame object with the pages
                                                  # listed in columns under the subreddit as the header
	
	masterlist = []
	sub = sreddits
	
	timeperiod = str(period) #period to take threads from, a string must be input into the function

	limit = str(resultlength) # how many threads to take
	
	for i in sub:
		user_agent = {'User-Agent': 'page id gatherer from /u/aguy'}
		time.sleep(2)
		r = requests.get('http://www.reddit.com/r/' + i + '/top/.json?t=' + timeperiod + '&' + 'limit=' + limit, headers = user_agent)
		stuff = r.json()

		entries = stuff['data']['children']

		post_ids = []

		for j in entries:
			post_ids.append(str(j['data']['id']))
		
			print post_ids
			
		masterlist.append(post_ids)
		
	return pd.DataFrame(masterlist, index = sreddits).transpose()
	

		
idtable = nested_maker(test, 'day', 10)

print idtable

# id_table.to_csv('sample_output.csv')

#idtable.to_csv .... write the command to convert the data to a csv file here along with the file path,
