#!/usr/local/bin/pypy

import sys
#sys.dont_write_bytecode = True

import string
import itertools
import signal
import multiprocessing

# If you try to write fast python code, you will have a baaaad time.

def generator(file,repl = {},upper = [],rperm=0,sfalse=0, s=(None,None)):
    ## Yes, this function is ugly, but we are trying to reduce function call overheads in python interpreter
    ## Each function call adds additional overhead into already slow performance of the interpreter.
    if 'ALL' in upper:
        upper = range(0,100)
    if len(upper) > 0 and len(repl) == 0: ## Only uppercase some words
        with open(file) as wordlist:
            for line in wordlist:
                out = list(line.rstrip())
                try:
                    for id in upper:
                        out[id] = string.upper(out[id])
                except:
                    pass
                yield ''.join(out)[slice(*s)]
    elif len(upper) == 0 and len(repl) > 0 and rperm == 0 and sfalse == 0: # fast REPL
        with open(file) as wordlist:
            for line in wordlist:
                out = line
                for el in repl:
                    out = out.replace(el,repl[el]).rstrip()
                yield out[slice(*s)]
    else:
        with open(file) as wordlist:
            if rperm == 1:
                for line in wordlist:
                    mlen = 0
                    for re in repl:
                        mlen += line.count(re)
                    for mask in itertools.product('01',repeat=mlen):
                        mid = 0
                        pl = list(line)
                        for el in range(len(pl)):
                            if pl[el] in repl:
                                if mask[mid] == '1':
                                    pl[el] = repl[pl[el]]
                                mid += 1
                            if el in upper:
                                pl[el] = string.upper(pl[el])
                        ot = ''.join(pl).rstrip()
                        if sfalse == 0:
                            yield ot[slice(*s)]
                        else:
                            if len(set(repl.keys()).intersection(set(string.lower(line)))) != 0:
                                yield ot[slice(*s)]
            else:
                for line in wordlist:
                    pl = list(line)
                    for el in range(len(pl)):
                        if pl[el] in repl:
                            pl[el] = repl[pl[el]]
                        if el in upper:
                            pl[el] = string.upper(pl[el])
                    ot = ''.join(pl).rstrip()
                    if (len(set(repl.keys()).intersection(set(string.lower(line)))) != 0) and sfalse == 1:
                        yield ot[slice(*s)]
                    elif sfalse == 0:
                        yield ot[slice(*s)]


def file_to_dictlist(file):
    dl = []
    with open(file) as a:
        for line in a.readlines():
            dl.append( eval(line.rstrip()))
    return dl

def stripped_openfile(handle):
    with open(handle) as file:
        for line in file:
            yield line.rstrip()

def bfgenerator(generate,length):
    for el in itertools.product(generate,repeat=length):
            yield ''.join(el)

def bf_L_generator(generate,tolength):
    for l in range(1,tolength+1):
        for el in itertools.product(generate,repeat=l):
                yield ''.join(el)

def specify_generator(elem):
    if type(elem) == str:
        return [elem]
    if type(elem) == dict:
        file = ''
        repl = {}
        upper = []
        rperm = 0
        sfalse = 0
        cf = ct = None
        s = (None,None)
        if elem.has_key('g') and len(elem) == 2:
            return bfgenerator(elem['g'],elem['l'])
        if elem.has_key('gl') and len(elem) == 2:
            return bf_L_generator(elem['gl'],elem['l'])
        if elem.has_key('f') and len(elem) == 1:
            return stripped_openfile(elem['f'])
        if elem.has_key('f'):
            file = elem['f']
        if elem.has_key('r'):
            repl = elem['r']
        if elem.has_key('rf'):
            repl = file_to_dictlist(elem['rf'])
        if elem.has_key('u'):
            upper = elem['u']
        if elem.has_key('ul'):
            upper = file_to_dictlist('ul')
        if elem.has_key('p'):
            rperm = 1
        if elem.has_key('i'):
            sfalse = 1
        if elem.has_key('s'):
            s = elem['s']
        return generator(file,repl,upper,rperm,sfalse,s)

def p(*args):
    gdef = []
    sys.stderr.write('[i] running rule: ' + str(args))
    for gen in args:
        gdef.append(specify_generator(gen))
    for el in itertools.product(*(gdef)):
        #sys.stdout.write(''.join(map(lambda x: x.rstrip(),el))+'\n')
        sys.stdout.write(''.join(el)+'\n')

def gen(argspec):
    gdef = []
    sys.stderr.write('[i] running rule: ' + str(argspec) + '\n')
    for gen in argspec:
        gdef.append(specify_generator(gen))
    for el in itertools.product(*(gdef)):
        #sys.stdout.write(''.join(map(lambda x: x.rstrip(),el))+'\n')
        sys.stdout.write(''.join(el)+'\n')

def initw():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def crack(pattern,NUMCPUS=2):
    i = 0
    pool = multiprocessing.Pool(processes=NUMCPUS,initializer=initw)
    pool.map(gen,pattern)

if __name__ == '__main__':
    import argparse
    desc ='''
    UNHash - rule based password cracker written for pypy\n
    Tonimir Kišasondi (c) 2012 -\n
    protip: SMP support in pypy cannot be interrupted with CTRL+C, use:\n
    ./unhash rulefile | cat\n
    to test the output.\n
    '''
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('RULE_FILE', help='The rulefile you want to run')
    args=parser.parse_args()
    u = 'u'
    f = 'f'
    r = 'r'
    p = 'p'
    i = 'i'
    g = 'g'
    gl = 'gl'
    l = 'l'
    s = 's'
    execfile(args.RULE_FILE)
    crack(RULES,NUMCPUS)
