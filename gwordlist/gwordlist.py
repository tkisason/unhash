#!/usr/bin/python
import string
import time


def cln(x):
    return x.replace("\n", "")


def red(x):
    if x in string.lowercase: return "a"
    if x in string.uppercase: return "A"
    if x in string.whitespace: return "_"
    if x in string.digits: return "0"
    return "#"


def l1red(x):
    return (''.join(map(red, cln(x))))


def l0red(x):
    x = l1red(x)
    bg = x[0]
    for i in x:
        if i != bg[-1]:
            bg += i
    return bg


def freq_an(input, fx={}):
    for elem in input:
        if fx.has_key(elem):
            fx[elem] += 1
        else:
            fx[elem] = 1
    return fx


def scrape_links_and_wordlistify(links, lower=False, verbose=1):
    import nltk
    import requests
    import string
    raw = ''
    wordlist = {}
    for site in links:
        try:
            if verbose == 1:
                print '[+] fetching data from: ', site
            if site.find('http://pastebin.com/') == 0:
                raw = requests.get(site.replace('http://pastebin.com/', 'http://pastebin.com/raw.php?i=')).content
            else:
                raw = requests.get(site).content
            if lower == False:
                l = string.translate(nltk.clean_html(raw), string.maketrans(string.punctuation, ' ' * 32)).split()
                freq_an(l, wordlist)
            else:
                l = string.lower(nltk.clean_html(raw))
                l = string.translate(l, string.maketrans(string.punctuation, ' ' * 32)).split()
                freq_an(l, wordlist)
        except:
            if verbose == 1:
                print '[-] Skipping url: ', site
    return wordlist


def google_wordlist(queries, results_per_query=5, lower=False, verbose=1):
    from google import search
    import random
    links = []
    num = 0
    for q in queries:
        try:
            print '[+] querying for: ', q
            links += [x for x in search(q, tld='hr', num=10, stop=results_per_query, pause=random.randrange(3, 12))][:results_per_query]
            time.sleep(random.randrange(3, 12))
        except:
            if verbose == 1:
                print '[-] google fails on query ', q
            time.sleep(random.randrange(3, 12))
    links = list(set(links))
    return scrape_links_and_wordlistify(links, lower)


if __name__ == '__main__':
    __program__ = 'gwordlist'
    __url__ = 'https://github.com/tkisason/unhash'
    __author__ = 'Tonimir Kisasondi <kisasondi@gmail.com>'
    __copyright__ = 'Copyright (c) 2012 - '
    __version__ = '0.6'
    import argparse
    import operator
    desc = 'Generate custom wordlists based on google queries and screen scrapes of N top links returned by google queries for each keyword'
    print '\n'+__program__+' '+__version__+' by '+__author__+'\n'+__copyright__
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('KEYWORDS_FILE', help='Load keywords from KEYWORDS_FILE, one line == one search query')
    parser.add_argument('OUTPUT_FILE', help='Your wordlist will be saved/appended to OUTPUT_FILE')
    parser.add_argument('-l', '--lowercase', help='Make sure all capitals are LOWERCASE, useful if you will use rules to mutate your wordlist', action='store_true')
    parser.add_argument('-w', '--weights', help='', action='store_true')
    parser.add_argument('-n', '--number', help='Use NUMBER of top google links for scraping instead of default 5 ', type=int, default=5)
    args = parser.parse_args()
    keywords = open(args.KEYWORDS_FILE, 'r').read().strip().split("\n")
    print '[+] Googling for keywords'
    owl = google_wordlist(keywords, int(args.number), args.lowercase)
    print '[+] Sorting wordlist according to word probability'
    sorted_wl = sorted(owl.iteritems(), key=operator.itemgetter(1), reverse=True)
    w = open(args.OUTPUT_FILE + '-words', 'w')
    n = open(args.OUTPUT_FILE + '-numbers', 'w')
    m = open(args.OUTPUT_FILE + '-misc', 'w')
    print '[+] Writing wordlist to :', args.OUTPUT_FILE, ', numbers will be in ', args.OUTPUT_FILE, '-numbers and the rest will be in', args.OUTPUT_FILE, '-misc'
    weight = ''
    for line in sorted_wl:
        if args.weights:
            weight = str('\t'+line[1])
        if l0red(line[0]) == 'a':
            w.write(line[0]+weight+'\n')
        elif l0red(line[0]) == '0':
            n.write(line[0]+weight+'\n')
        else:
            m.write(line[0]+weight+'\n')
    w.close()
    n.close()
    m.close()
    print '[+] Done!'
