REVISION HISTORY
================

Current version is v1.1, 22 September 2015


v1: 15 September 2015
---------------------
Barely functional first version.

v1.1: 22 September 2015
-----------------------
Cleaned up a fair amount. More logging naunces available. Docstrings. Processes command-line arguments. Can manually sort the tweet archive with the --sort-archive command-line option.



FUTURE PLANS
============
* Authenticate via the script itself?
* Spit out error info to stderr instead of stdout.
* Abstract the logger more: specify output target.
* Abstract more hardcoded values to command-line options.

KNOWN BUGS
==========
* Reports an error (when verbose) even after posting to Twitter.