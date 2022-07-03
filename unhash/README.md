## UNHash - rule based password cracker written for pypy
###### Tonimir Kišasondi (c) 2012 -

_Protip_: SMP support in `pypy` cannot be interrupted with <kbd>CTRL</kbd>+<kbd>C</kbd>, use `./unhash rulefile | cat` to test the output.

###Usage:

```bash
pypy unhash.py rulefile | john --stdin ....
```

You can test the script with:

```bash
pypy unhash.py rulefile | cat
```

For examples and syntax see:

* [examples.uhr](https://github.com/tkisason/unhash/blob/master/unhash/examples.uhr) - where the complete syntax is shown  
* [wordlists.uhr](https://github.com/tkisason/unhash/blob/master/unhash/wordlists.uhr) - which shows a basic wordlist attack with multiple dictionaries  
* [targeted.uhr](https://github.com/tkisason/unhash/blob/master/unhash/targeted.uhr) - which uses the [keywords.txt](https://github.com/tkisason/unhash/blob/master/unhash/keywords.txt) file to create a targeted attack against a small password list  
* [rulebased.uhr](https://github.com/tkisason/unhash/blob/master/unhash/rulebased.uhr) - which is an optimized rule based exhaustive search, which should perform better then bruteforce attacks
