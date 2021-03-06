REVISION HISTORY
================

Current version is v1.4, 17 January 2016


v1: 15 September 2015
---------------------
Barely functional first version.

v1.1: 22 September 2015
-----------------------
* Cleaned up a fair amount.
* More logging naunces available.
* Docstrings.
* Processes command-line arguments.
* Can manually sort the tweet archive with the --sort-archive command-line option.

v1.2: 29 September 2015
----------------------
* Should now wait if rate limit is exceeded.
* Additional command-line arguments: -x, --extra-material: for saving rejected text that can't be tweeted.
* Additional command-line arguments: -a, --archive: for specifying the location of the tweets archive.
* Slightly better PEP8 compliance.
* The march toward further abstraction continues.

v1.21: 7 October 2015
---------------------
* Pulled the logging code out to a separate module, since I'm winding up using it in multiple scripts.
  * patrick_logger.py is currently the only script in the library I'm developing at https://github.com/patrick-brian-mooney/personal-library.
    * You can get it there if you need it. 
* Minor documentation updates.

v1.3: 7 October 2015
--------------------
* The script may now generate tweets of up to six sentences.
* This only happens when -x or --extra-material-archive is specified onthe command line.
* This has the effect of dumping material to the extra material archive more quickly. I'm OK with that.

v1.3: 10 October 2015
---------------------
* No version number bump. Only tiny changes.
* No more than four sentences in a tweet.
* Small updates for PEP8 compliance thanks to pylint.

v1.4: 17 January 2016
---------------------
* Converted from Python 2 to Python 3
  * This eases the burden of actively maintaining both environments on my laptop.
  * It also means there's less setup to do when I disto-hop.

FUTURE PLANS
============
* Authenticate via the script itself?
* Spit out error info to stderr instead of stdout.
* Abstract the logger more: specify output target.
* Abstract more hardcoded values to command-line options.

KNOWN BUGS
==========
* Reports an error (when verbose) even after posting to Twitter. (since at least v1.1)