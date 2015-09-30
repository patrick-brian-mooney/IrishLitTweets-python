#!/usr/bin/env python
"""
  ./generate.py [options]

If you're reading this statement, be aware that this is early-development code
that's nowhere near complete and not really intended for public use. However,
feedback is most welcome. See http://patrickbrianmooney.nfshost.com/~patrick/contact.html 

This script is by Patrick Mooney. It generates tweets based on writing I did as
a teaching assistant for a course on Irish literature. More information about
the script is available at http://is.gd/IrishLitAutoTweets. More technically
oriented information is available at http://is.gd/IrishLitAutoTweetsTechnical.

It won't do anything useful unless you set it up properly. See the above
websites for more information about that. Currently, this script is only set up
to be useful for me.

CURRENTLY AVAILABLE OPTIONS

  -h, --help
      Display this help message.

  --sort-archive
      Sort the tweet archive and exit. There's no obvious benefit to doing so,
      although it might get you the kind of satisfaction that people who like
      things to be sorted feel when things are sorted, if you are the kind of
      person who likes it when things are sorted. If you specify multiple
      options including --sort-archive, other options should come before it.

  -x PATH/TO/FILE, --extra-material=/PATH/TO/FILE
      Specify a full pathname for a file where rejected tweets will be kept.
      generate.py may generate multiple chunks of text before finding one
      \"acceptable\"; this is usually because the generated chunks of text are
      too short or too long. If you want to save these chunks of text, use this
      option to specify a file where they will accumulate. This may be useful
      if you have some other script that consumes them in some way. generate.py
      NEVER (intentionally) erases text from this file, so if you specify this
      option and nothing else is cleaning it out for you, you will need to clean
      it out just resign yourself to it growing boundlessly.
  
  -v, --verbose
      Increase the verbosity of the script, i.e. get more output. Can be
      specified multiple times to make the script more and more verbose.
      Current verbosity levels are defined below & are subject to change in
      future versions of the script. 

  -q, --quiet
      Decrease the verbosity of the script. You can mix -v and -q, bumping the 
      verbosity level up and down as the command line is processed, but really,
      what are you doing with your life?

 CURRENT VERBOSITY LEVELS (unchanged since v1.1)

  -1    Do not display any messages at all.
   0    Display only error messages.
   1    Talk in general terms about what the script is doing.
   2    Give more detail about processing command-line options and about
        interacting with Twitter.
   3    Currently equivalent to level 2.
   4    Also explicitly say that the log_it() function was called. This will
        probably double or triple the size of the log. It will certainly produce
        three times as many lines.

Currently, setting the verbosity level below -1 is equivalent to setting it to
-1, and setting it above 4 is equivalent to setting it to 4. The meanings of
different verbosity levels are subject to change in future versions of
generate.py.

This script requires tweepy, a module that handles Twitter authentication. Try
typing
    pip install tweepy
or
    sudo pip install tweepy
if it's not installed already.

Some current problems:
    * no way to authenticate via the script itself
    * consumer secret is visible in script
    * little to no error checking
    * not enough is configurable via the command line
    
This is v1.2. A version number above 1 doesn't mean it's ready for the public,
just that there have been multiple versions.
http://patrickbrianmooney.nfshost.com/~patrick/projects/IrishLitTweets/

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.

If this is your first time running this script, it's a REALLY GOOD IDEA to read
all of this text, including whatever might have scrolled off the top of your
screen.
"""

__author__ = "Patrick Mooney, http://patrickbrianmooney.nfshost.com/~patrick/"
__version__ = "$v1.2 $"
__date__ = "$Date: 2015/09/22 11:56:00 $"
__copyright__ = "Copyright (c) 2015 Patrick Mooney"
__license__ = "GPL v3, or, at your option, any later version"

import subprocess
import pprint
import getopt
import sys
import datetime

import tweepy

# Set up default values

# Can set the starting level above zero explicitly when debugging, esp. when debugging command-line options
verbosity_level = 0
extra_material_archive = ''  # An empty string means don't archive (i.e., discard) material that's too long.
tweet_archive_path = '/150/tweets.txt'  # If you don't like it, use -a on the command line

# Functions

def log_it(message,minimum_level=1):
    """Add a message to the log if verbosity_level is at least minimum_level.
    Currently, the log goes to standard output.
    """
    if verbosity_level >= 4: # set verbosity to at least 4 to get this message output in the debug log
        print "\nDEBUGGING: function log_it() called"
    if verbosity_level >= minimum_level:
        print(message)

def print_usage():
    log_it("INFO: print_usage() was called")
    print(__doc__)

def sort_archive():
    """Sort the tweet archive. There's no obvious benefit to doing so. Call the script
    with the --sort-archive flag to do this. Currently, this does not ever happen
    automatically, but that might change in the future.
    """
    log_it("INFO: sort_archive() was called")
    try:
        tweet_archive = open(tweet_archive_path,'r+')
    except IOError:
        log_it("ERROR: can't open tweet archive file.", 0)
        sys.exit(3)
    try:
        all_tweets = tweet_archive.readlines() # we now have a list of strings
        log_it("DEBUGGING: Tweets archive successfully opened",2)
        log_it("INFO:   Current size of tweets archive is " + str(tweet_archive.tell()) + " bytes.")
        log_it("INFO:   And it is currently " + str(datetime.datetime.now()))
        log_it("INFO: About to sort",2)
        all_tweets.sort()
        tweet_archive.seek(0)
        log_it("DEBUGGING: About to start writing.", 2)
        for a_tweet in all_tweets:
            tweet_archive.write(a_tweet.strip() + "\n")
        log_it("DEBUGGING: Wrote all the tweets back to the archive.", 2)
        tweet_archive.truncate() # This is probably unnecessary: unless leading/trailing whitespace has crept into the tweets, the new file should be the same size as the old one. Still, better safe than sorry. But this is why a high debug level is needed to see this message.
        log_it("DEBUGGING: Truncated the tweet archive file.", 4)
        tweet_archive.close()
        log_it("DEBUGGING: Closed the tweet archive file.", 2)
    except IOError:
        log_it("ERROR: Trouble operating on tweet archive file.", 0)

def get_a_tweet():
    """Find a tweet. Keep trying until we find one that's an acceptable length. This
    function doesn't check to see if the tweet has been tweeted before.
    """
    log_it("INFO: finding a tweet ...")
    the_length = 160
    the_tweet = ''
    while not (45 < the_length < 141):
        if the_tweet and extra_material_archive:
            try:
                extra_material_archive_file = open(extra_material_archive,'a')
                extra_material_archive_file.write(the_tweet + ' ')
                extra_material_archive_file.close()
                log_it("Wrote tweet to extra material archive",2)
            except IOError: # and others?
                log_it("Could not write extra material to archive",0)
        the_tweet = subprocess.check_output(["dadadodo -c 1 -l /150/chains.dat -w 10000"],shell=True).strip()
        the_length = len(the_tweet)
        log_it("\nINFO:  The tweet generated was: " + the_tweet + "\nINFO:     and the length of that tweet is: " + str(the_length))
    log_it("OK, that's it, we found one")
    if extra_material_archive:
        try:
            extra_material_archive_file = open(extra_material_archive,'a')
            extra_material_archive_file.write('\n\n') # Start a new paragraph in the extra material archive.
            extra_material_archive_file.close()
        except IOError: # and others?
            log_it("Could start new paragraph in extra material archive",0)
    return the_tweet
    

# Script's execution starts here

log_it('INFO: command line is: ' + pprint.pformat(sys.argv) + "\nINFO: Parsing command line")
log_it('Starting verbosity level is ' + str(verbosity_level))

# Parse command-line options, if there are any
if len(sys.argv) > 1: # The first option in argv, of course, is the name of the program itself.
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vhqx:a:', ['verbose','help','quiet','sort-archive','extra-material=','tweet-archive='])
        log_it('INFO: options returned from getopt.getopt() are: ' + pprint.pformat(opts),2)
    except getopt.GetoptError:
        log_it('INFO: Error in command-line arguments; exiting to shell')
        print_usage()
        sys.exit(2)
    log_it('INFO: detected number of command-line arguments is ' + str(len(sys.argv)),2)
    for opt,args in opts:
        log_it('Processing option ' + str(opt),2)
        if opt in ('-h', '--help'):
            log_it('INFO: ' + opt + ' invoked, printing usage message')
            print_usage()
            sys.exit()
        elif opt in ('-v', '--verbose'):
            verbosity_level += 1
            log_it('INFO: ' + opt + ' invoked, added one to verbosity level\n     Verbosity level is now ' + str(verbosity_level))
        elif opt in ('-q', '--quiet'):
            log_it('INFO: ' + opt + ' invoked, decreasing verbosity level by one\n     Verbosity level is about to drop to ' + str(verbosity_level-1))
            verbosity_level -= 1
        elif opt in ('-x', '--extra-material'):
            log_it('INFO: ' + opt + ' invoked; extra material archive initialized to ' + args,2)
            extra_material_archive = args
        elif opt in ('-a', '--archive'):
            log_it('INFO: ' + opt + ' invoked; tweet archive set to ' + args,2)
            tweet_archive_path = args
        elif opt == '--sort-archive':
            log_it('INFO: --sort-archive specified; sorting and exiting')
            sort_archive()
            sys.exit()
else:
    log_it('DEBUGGING: No command-line parameters',2)

log_it('DEBUGGING: verbosity_level after parsing command line is ' +str(verbosity_level))

# All right, start processing
got_it = False

while not got_it:
    the_tweet = get_a_tweet()
    if the_tweet in open(tweet_archive_path).read():    # Incidentally, this is a really bad idea if the tweets log ever gets very big
        log_it("That was already tweeted! Trying again ...\n\n\n")
    else:
        got_it = True
        log_it("Aaaaaand that one's new. Tweeting it ...\n\n")


# Now, post the tweet.
# This next code paragraph is partially based on a tutorial at nihkil's blog, http://nodotcom.org/python-twitter-tutorial.html

# If you're using this script, you'll have to fill in the values below. See nihkil's blog post for a sample of how to get these keys, tokens, and secrets.
cfg = { 
    'consumer_key'        : 'FILL ME IN',
    'consumer_secret'     : 'FILL ME IN',
    'access_token'        : 'FILL ME IN',
    'access_token_secret' : 'FILL ME IN'
    }
try:
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    status = api.update_status(status=the_tweet)
except tweepy.error.TweepError:
    pass # for now, we just want to trap this silently, not act on it; later, we'll log it explicitly. Note that this error will currently get recorded indirectly in the log anyway.
else:
    # If everything worked, add the tweet to the tweet archive.
    open(tweet_archive_path,'a').write(the_tweet + "\n")
finally:
    log_it('DEBUGGING:  Authorization object:\n' + pprint.pformat(vars(auth)) + '\nDEBUGGING:  API object:\n' + pprint.pformat(vars(api)) + '\nDEBUGGING:  Status object:',2)
    try:
        log_it(pformat.pprint(vars(status)),2)
    except NameError:
        log_it('  Not created, because an error occurred',2)

# We're done.