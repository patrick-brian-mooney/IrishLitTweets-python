#!/usr/bin/env python3
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

COMMAND-LINE OPTIONS

  -h, --help
      Display this help message.

  -a PATH/TO/FILE, --archive PATH/TO/FILE (since v1.2)
      Specify the location of the tweets archive file. If not used, it defaults
      to /150/tweets.txt. If that's not a great location for you, then use the
      -a or --archive option.

  --sort-archive
      Sort the tweet archive and exit. There's no obvious benefit to doing so,
      although it might get you the kind of satisfaction that people who like
      things to be sorted feel when things are sorted, if you are the kind of
      person who likes it when things are sorted. If you specify multiple
      options including --sort-archive, other options should come before it.

  -x PATH/TO/FILE, --extra-material=/PATH/TO/FILE (since v1.2)
      Specify a full pathname for a file where rejected tweets will be kept.
      generate.py may generate multiple chunks of text before finding one
      \"acceptable\"; this is usually because the generated chunks of text are
      too short or too long. If you want to save these chunks of text, use this
      option to specify a file where they will accumulate. This may be useful
      if you have some other script that consumes them in some way. generate.py
      NEVER (intentionally) erases text from this file, so if you specify this
      option and nothing else is cleaning it out for you, you will need to clean
      it out manually or just resign yourself to it growing boundlessly.

      Since v1.3, this option also makes the script try (most of the time) to
      generate more than one sentence: without this option, the script just
      asks DadaDodo for a single sentence. With this option, the script will
      try to generate anywhere between one and four sentences. This has the side
      effect of producing a lot more material for the extra material archive.

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
    * no way to authenticate with Twitter via the script itself
    * not enough error checking

This is v1.4. A version number above 1 doesn't mean it's ready for the public,
just that there have been multiple versions.
http://patrickbrianmooney.nfshost.com/~patrick/projects/IrishLitTweets/

This program is licensed under the GPL v3 or, at your option, any later
version. See the file LICENSE.md for a copy of this licence.

If this is your first time running this script, it's a REALLY GOOD IDEA to read
all of this text, including whatever might have scrolled off the top of your
screen.
"""

__author__ = "Patrick Mooney, http://patrickbrianmooney.nfshost.com/~patrick/"
__version__ = "$v1.4 $"
__date__ = "$Date: 2016/09/22 20:44:00 $"
__copyright__ = "Copyright (c) 2015-16 Patrick Mooney"
__license__ = "GPL v3, or, at your option, any later version"

import subprocess, pprint, getopt, sys, datetime, random

import patrick_logger # From https://github.com/patrick-brian-mooney/personal-library
import social_media
from social_media_auth import IrishLitTweets_client

import sentence_generator as sg

# Set up default values
# patrick_logger.verbosity_level = 4    # uncomment this to set the starting verbosity level
chains_file = '/150/2chains.dat'        # The location of the compiled textual data.
extra_material_archive_path = ''       # Full path to a file. An empty string means don't archive (i.e., do discard) material that's too long.
tweet_archive_path = '/150/tweets.txt'

patrick_logger.log_it("INFO: WE'RE STARTING, and the verbosity level is " + str(patrick_logger.verbosity_level), 0)

genny = sg.TextGenerator('IrishLitTweets generator')
genny.chains.read_chains(chains_file)

# Functions
def print_usage():
    """Print a usage message to the terminal"""
    patrick_logger.log_it("INFO: print_usage() was called")
    print(__doc__)

def sort_archive():
    """Sort the tweet archive. There's no obvious benefit to doing so. Call the script
    with the --sort-archive flag to do this. Currently, this does not ever happen
    automatically, but that might change in the future.
    """
    patrick_logger.log_it("INFO: sort_archive() was called")
    try:
        tweet_archive = open(tweet_archive_path, 'r+')
    except IOError:
        patrick_logger.log_it("ERROR: can't open tweet archive file.", 0)
        sys.exit(3)
    try:
        all_tweets = tweet_archive.readlines() # we now have a list of strings
        patrick_logger.log_it("DEBUGGING: Tweets archive successfully opened", 2)
        patrick_logger.log_it("INFO:   Current size of tweets archive is " + str(tweet_archive.tell()) + " bytes.")
        patrick_logger.log_it("INFO:   And it is currently " + str(datetime.datetime.now()))
        patrick_logger.log_it("INFO: About to sort", 2)
        all_tweets.sort()
        tweet_archive.seek(0)
        patrick_logger.log_it("DEBUGGING: About to start writing.", 2)
        for a_tweet in all_tweets:
            tweet_archive.write(a_tweet.strip() + "\n")
        patrick_logger.log_it("DEBUGGING: Wrote all the tweets back to the archive.", 2)
        tweet_archive.truncate() # This is probably unnecessary: unless leading/trailing whitespace has crept into the tweets, the new file should be the same size as the old one. Still, better safe than sorry. But this is why a high debug level is needed to see this message.
        patrick_logger.log_it("DEBUGGING: Truncated the tweet archive file.", 4)
        tweet_archive.close()
        patrick_logger.log_it("DEBUGGING: Closed the tweet archive file.", 2)
    except IOError:
        patrick_logger.log_it("ERROR: Trouble operating on tweet archive file.", 0)

def get_a_tweet():
    """Find a tweet. Keep trying until we find one that's an acceptable length. This
    function doesn't check to see if the tweet has been tweeted before; it just
    finds a tweet that's in acceptable length parameters.

    By default, this procedure tries to generate a single-sentence chunk of text,
    but note that if and only if -x or --extra-material-archive is in effect, the
    procedure asks for a random number of sentences between one and six. Most
    chunks of text generated from more than one sentence will be too long, which
    means that material accumulates in the archive faster.
    """
    patrick_logger.log_it("INFO: finding a tweet ...")
    the_length = 160
    the_tweet = ''
    sentences_requested = 1
    while not 45 < the_length < 141:
        if extra_material_archive_path:
            sentences_requested = random.choice(list(range(1, 4)))
            patrick_logger.log_it("\nINFO: We're asking for %d sentences." % sentences_requested, 2)
        if the_tweet and extra_material_archive_path:
            try:
                extra_material_archive_path_file = open(extra_material_archive_path, 'a')
                extra_material_archive_path_file.write(the_tweet + ' ')
                extra_material_archive_path_file.close()
                patrick_logger.log_it("INFO: Wrote tweet to extra material archive", 2)
            except IOError: # and others?
                patrick_logger.log_it("ERROR: Could not write extra material to archive", 0)
        the_tweet = genny.gen_text(sentences_desired=sentences_requested, paragraph_break_probability=0)
        the_tweet = the_tweet.strip()
        the_length = len(the_tweet)
        patrick_logger.log_it("\nINFO:  The tweet generated was: " + the_tweet + "\nINFO:     and the length of that tweet is: " + str(the_length))
    patrick_logger.log_it("OK, that's it, we found one")
    if extra_material_archive_path:    # End the paragraph that we've been accumulating during this run.
        try:
            extra_material_archive_path_file = open(extra_material_archive_path, 'a')
            extra_material_archive_path_file.write('\n\n') # Start a new paragraph in the extra material archive.
            extra_material_archive_path_file.close()
        except IOError: # and others?
            patrick_logger.log_it("Couldn't start new paragraph in extra material archive", 0)
    return the_tweet


# Script's execution starts here

patrick_logger.log_it('INFO: command line is: ' + pprint.pformat(sys.argv) + "\nINFO: Parsing command line")
patrick_logger.log_it('Starting verbosity level is ' + str(patrick_logger.verbosity_level))

# Parse command-line options, if there are any
if len(sys.argv) > 1: # The first option (index 0) in argv, of course, is the name of the program itself.
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vhqx:a:', ['verbose', 'help', 'quiet', 'sort-archive', 'extra-material=', 'tweet-archive='])
        patrick_logger.log_it('INFO: options returned from getopt.getopt() are: ' + pprint.pformat(opts), 2)
    except getopt.GetoptError:
        patrick_logger.log_it('ERROR: Bad command-line arguments; exiting to shell')
        print_usage()
        sys.exit(2)
    patrick_logger.log_it('INFO: detected number of command-line arguments is ' + str(len(sys.argv)), 2)
    for opt, args in opts:
        patrick_logger.log_it('Processing option ' + str(opt), 2)
        if opt in ('-h', '--help'):
            patrick_logger.log_it('INFO: ' + opt + ' invoked, printing usage message')
            print_usage()
            sys.exit()
        elif opt in ('-v', '--verbose'):
            patrick_logger.verbosity_level += 1
            patrick_logger.log_it('INFO: ' + opt + ' invoked, added one to verbosity level\n     Verbosity level is now ' + str(patrick_logger.verbosity_level))
        elif opt in ('-q', '--quiet'):
            patrick_logger.log_it('INFO: ' + opt + ' invoked, decreasing verbosity level by one\n     Verbosity level is about to drop to ' + str(patrick_logger.verbosity_level-1))
            patrick_logger.verbosity_level -= 1
        elif opt in ('-x', '--extra-material'):
            patrick_logger.log_it('INFO: ' + opt + ' invoked; extra material archive initialized to ' + args, 2)
            extra_material_archive_path = args
        elif opt in ('-a', '--archive'):
            patrick_logger.log_it('INFO: ' + opt + ' invoked; tweet archive set to ' + args, 2)
            tweet_archive_path = args
        elif opt == '--sort-archive':
            patrick_logger.log_it('INFO: --sort-archive specified; sorting and exiting')
            sort_archive()
            sys.exit()
else:
    patrick_logger.log_it('DEBUGGING: No command-line parameters', 2)

patrick_logger.log_it('DEBUGGING: patrick_logger.verbosity_level after parsing command line is ' +str(patrick_logger.verbosity_level))

# All right, start processing
got_it = False

while not got_it:
    the_tweet = get_a_tweet()
    if the_tweet in open(tweet_archive_path).read():
        patrick_logger.log_it("That was already tweeted! Trying again ...\n\n\n")
    else:
        got_it = True
        patrick_logger.log_it("Aaaaaand that one's new. Tweeting it ...\n\n")

# Now, post the tweet.
status = social_media.post_tweet(the_tweet, IrishLitTweets_client)
# If everything worked, add the tweet to the tweet archive.
open(tweet_archive_path, 'a').write(the_tweet + "\n")
patrick_logger.log_it(pprint.pformat(vars(status)), 2)

# We're done.
