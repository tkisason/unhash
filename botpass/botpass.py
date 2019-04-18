#!/usr/bin/python

import urllib2
import json
import collections
import sys
import operator

userpass = collections.defaultdict(int)
ips = collections.defaultdict(int)

PWD = open('botnet-userpass.log', 'w')
PWDL = open('botnet-userpass-len.log', 'w')
IPS = open('botnet-ipranges.log', 'w')


def get_page(n=1):
    url = 'http://sshpot.com/api/ssh_logins.json?page='+str(n)
    return urllib2.urlopen(url).read()


def collect_data():
    data = ''
    n = 1
    print '[+] downloading honeypot data'
    while data is not None:
        page = get_page(n)
        data = json.loads(page)['data']
        n += 1
        sys.stdout.write('.')
        sys.stdout.flush()
        if data is None:
            break
        else:
            for el in data:
                userpass[(el['username'], el['password'])] += 1
                ips[el['remote_addr']] += 1
    print '\n[+] done'


def sort_userpass(item, sep=' '):
    SORT = sorted(item.iteritems(), key=operator.itemgetter(1), reverse=True)
    for el in SORT:
        try:
            PWDL.write(el[0][0] + sep + el[0][1] + sep + str(el[1]) + '\n')
            PWD.write(el[0][0]+sep+el[0][1]+'\n')
        except:
            print '[!] skipping pair ', el[0]
    PWD.close()
    PWDL.close()


def sort_ip(item, sep=' '):
    SORT = sorted(item.iteritems(), key=operator.itemgetter(1), reverse=True)
    for el in SORT:
        try:
            IPS.write(el[0]+sep+str(el[1])+'\n')
        except:
            print '[!] skipping IP ', el[0]
    IPS.close()


if __name__ == '__main__':
    print '[+] collecting data from sshpot honeypots'
    collect_data()
    print '[+] dumping users/passes'
    sort_userpass(userpass)
    print '[+] dumping IPs'
    sort_ip(ips)
