#!/usr/bin/env python
"""
If you're reading this statement, be aware that this is early-development code
that's nowhere near complete and not really intended for public exhibition.

This script is by Patrick Mooney. It generates tweets based on writing I did as
a teaching assistant for a course on Irish literature. It's released under a
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
More information about the script is available at
http://is.gd/IrishLitAutoTweets. More technically oriented information is
available at http://is.gd/IrishLitAutoTweetsTechnical.

It won't do anything useful unless you set it up properly. See the above
websites for more information about that. Currently, this script is only set up
to be useful for me.

This script requires tweepy, a module that handles Twitter authentication. Try
typing
    pip install tweepy
or
    sudo pip install tweepy
if it's not installed already.

Some current problems:
	* no way to authenticate via the application
	* consumer secret is visible in script
	* no error checking
"""

import subprocess
import tweepy

debugging = True

def get_a_tweet():
	if debugging:
		print "DEBUGGING: finding a tweet ..."
	the_length = 160
	while not the_length in range(46,141):
		the_tweet = subprocess.check_output(["dadadodo -c 1 -l /150/chains.dat -w 10000"],shell=True).strip()
		the_length = len(the_tweet)
		if debugging:
			print "\nDEBUGGING:  The tweet generated was: ", the_tweet
			print "DEBUGGING:     and the length of that tweet is: ",the_length
	if debugging:
		print "OK, that's it, we found one"

	return the_tweet
	
got_it = False

while not got_it:
	the_tweet = get_a_tweet()
	if the_tweet in open('/150/tweets.txt').read():	# Incidentally, this is a really bad idea if the tweets log ever gets very big
		if debugging:
			print "That was already tweeted! Trying again ...\n\n\n"
	else:
		got_it = True
		if debugging:
			print "OK, that one's new. Tweeting it ...\n\n"


# Now, post the tweet.
# This next code paragraph (currently nine lines) are based on a tutorial at nihkil's blog, http://nodotcom.org/python-twitter-tutorial.html

cfg = { 
    "consumer_key"        : 'cu1M5PSoCjrjGUy5zK44Q7RXz',
    "consumer_secret"     : 'R4MMAjTFFjb4HYvySTDShZ6cBGUouxqIY2OsPTrNrL3HybdLYz',
    "access_token"        : '98912248-JwFQGrHeGLhHMW59kKjbewA7259rOT0hwkzPkZ89X',
    "access_token_secret" : 'pf9ZTk9WkUYYn7Ev5UxhbwyRoDH2tdgCP015Esuzwtqbx'
    }
auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
api = tweepy.API(auth)
status = api.update_status(status=the_tweet)

# That last code paragraph should have some debugging code

# In the publicly accessible version of this script, the values above have been revoked.

# Add the tweet to the list of tweets 
open('/150/tweets.txt','a').write(the_tweet)