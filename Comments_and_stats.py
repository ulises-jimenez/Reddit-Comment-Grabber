import praw 
import requests
import pandas as pd
import time
from datetime import datetime


subreddits = ["pics", "soccer", "nba", "videos", "hiphopheads", "fitness", "running", "nintendo", 
				"cscareerquestions", "askreddit"] # list of subreddits to be used in experiment
				
timeperiod = 'day' #period to take threads from

limit = '10' # how many threads to take

test = ['nba', 'soccer'] #test

post_ids = [] # list of pages

page_ids = ['2intlp','2inrz2'] #test

def commetinfo(idlist):
	
	user_agent = ("Top 10 comment scraper by /u/aguy")

	r = praw.Reddit(user_agent) #opens connection with reddit api
	
	
	
	body_list = []
	reply_count = []
	scores = []
	thread_vote_count = [] #??? this needs to be inserted into each comment's tuple
	comment_vote_count = []
	time_posted_after_thread = [] # in epoch seconds
	#user_comment_karma = []
	comment_author = []
	
	thread_comment_count = []  #??? this needs to be inserted into each comment's tuple
	comment_length = []
	sub = []
	scribers = []
	
	for i in idlist:
		submission = r.get_submission(submission_id = i) # navigates to wanted page
		comments = submission.comments #grabs comments from page
		
		flatcomments = praw.helpers.flatten_tree(comments) #final comment list including replies
		
		
		for i in comments: #adds comment to a list
			
			try:
			
				if bool(i.author):
					
					body_list.append(i.body)
					reply_count.append(len(i.replies))
					scores.append(i.score)
					comment_vote_count.append(i.downs + i.ups)
					time_posted_after_thread.append( i.created_utc - submission.created_utc)
					
					#user_comment_karma.append(i.author.comment_karma)
					
					comment_author.append(i.author)
					comment_length.append(len(i.body))
					thread_vote_count.append(submission.ups + submission.downs)#??? this needs to be inserted into	each comment's tuple
					thread_comment_count.append(submission.num_comments)
					sub.append(i.subreddit.display_name)
					scribers.append(i.subreddit.subscribers)
					print i 
					
				else:
								pass
			except AttributeError:
				pass
				
		print "%r is done" % i

	mlist = zip(body_list,
	reply_count,
	scores,
	thread_vote_count, 
	comment_vote_count,
	time_posted_after_thread,
	comment_author, 
	thread_comment_count, 
	comment_length, sub, scribers)

	data = pd.DataFrame(mlist, columns = ['body_list',
	'reply_count',
	'scores',
	'thread_vote_count', 
	'comment_vote_count',
	'time_posted_after_thread',
	'comment_author', 
	'thread_comment_count', 
	'comment_length', 'sub_reddit', 'subreddit_ subscribers'])
	print data
	return data
	
	
def nested_id_maker(sreddits, period, resultlength):

	sub = sreddits
	timeperiod = str(period) #period to take threads from, a string must be input into the function
	post_ids = []
	limit = str(resultlength) # how many threads to take
	
	for i in sub:
		user_agent = {'User-Agent': 'page id gatherer from /u/aguy'}
		time.sleep(2)
		r = requests.get('http://www.reddit.com/r/' + i + '/top/.json?t=' + timeperiod + '&' + 'limit=' + limit, headers = user_agent)
		stuff = r.json()

		entries = stuff['data']['children']

		for j in entries:
			post_ids.append(str(j['data']['id']))
	
	print post_ids
	return post_ids

a = nested_id_maker(subreddits, 'day', 5)

b = commetinfo(a)

#b.to_csv('final_table.csv', index = False, header = True)
