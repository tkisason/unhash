UNHash - rule based password cracker written for pypy
Tonimir Kišasondi (c) 2012 -
protip: SMP support in pypy cannot be interrupted with CTRL+C, use:
./unhash rulefile | cat to test the output.

Usage:

pypy unhash.py rulefile | john --stdin ....

You can test the script with:

pypy unhash.py rulefile | cat


For examples and syntax see:

examples.uhr - where the complete syntax is shown
wordlists.uhr - which shows a basic wordlist attack with multiple dictionaries
targeted.uhr - which uses the keywords.txt file to create a targeted attack against a small password list
rulebased.uhr - which is an optimized rule based exhaustive search, which should perform better then bruteforce attacks



