REVISION HISTORY
================

Current version is v1.2, 29 September 2015


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


FUTURE PLANS
============
* Authenticate via the script itself?
* Spit out error info to stderr instead of stdout.
* Abstract the logger more: specify output target.
* Abstract more hardcoded values to command-line options.

KNOWN BUGS
==========
* Reports an error (when verbose) even after posting to Twitter. (since at least v1.1)