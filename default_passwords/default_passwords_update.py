#!/usr/bin/python

import requests
import BeautifulSoup
import collections

separator = '\t'
pwd_list = collections.defaultdict(int)
rpllist = {'(none)':'','n/a':'','(any 3 characters)':'adm','(exclamation)':'!','Type User:':'','smcadmin OR administrator OR (none)':'smcadmin','the same all over':'Administrator','often blank':'',' (caps count !)':'','(no password by default)':'',' (cannot be changed)':'','(any)':'root','(blank)':'','(NULL)':'',' (or blank)':''}
passlist = ['the 6 last digit of the MAC adress','and 2000 Series','l=b[b.length-1].previousS','[email&nbsp;protected]','![CDATA[ */','(function(){try{var s,a,i,j,r','See notes','(touch password)','(see notes)','**ADMIN (**23646)','**CONFIG (266344)','bcpb+serial#','hostname/ip address','Web Browser only','2 + last 4 of Audio Server chasis','public/private/secret','no default password','(caclulated)','serial number','(created)','(see note)','serial-number','(hostname/ipaddress)','Last 4 digits of VIN']

#mild code bloat, but i want to reuse the functions later
def get_phenoelit_list():
    url = 'http://www.phenoelit.org/dpl/dpl.html'
    data = requests.get(url).text
    soup = BeautifulSoup.BeautifulSoup(data)
    table = soup.find("table")
    for row in table.findAll('tr'):
        cells = row.findAll('td')
        username = cells[4].text
        password = cells[5].text
        line = username + separator + password
        for el in rpllist:
            line = line.replace(el,rpllist[el])
        add = 1
        for el in passlist:
            if line.find(el) >= 0:
                add = 0
        if add == 1:
            pwd_list[line] += 1

def get_liquidmatrix_list():
    url = 'http://www.liquidmatrix.org/blog/default-passwords/'
    data = requests.get(url).text
    soup = BeautifulSoup.BeautifulSoup(data)
    table = soup.find("table")
    for row in table.findAll('tr')[1:]: # skip th
        cells = row.findAll('td')
        username = cells[4].text
        password = cells[5].text
        line = username + separator + password
        for el in rpllist:
            line = line.replace(el,rpllist[el])
        add = 1
        for el in passlist:
            if line.find(el) >= 0:
                add = 0
        if add == 1:
            pwd_list[line] +=1

def get_securityoverride_list():
    url = 'http://securityoverride.org/default-password-list/'
    data = requests.get(url).text
    soup = BeautifulSoup.BeautifulSoup(data)
    table = soup.find("table",{'id':'sorttable'})
    for row in table.findAll('tr')[1:]: # skip th
        cells = row.findAll('td')
        username = cells[3].text
        password = cells[4].text
        line = username + separator + password
        for el in rpllist:
            line = line.replace(el,rpllist[el])
        add = 1
        for el in passlist:
            if line.find(el) >= 0:
                add = 0
        if add == 1:
            pwd_list[line] +=1


def get_dexcms_list():
    url = 'http://dexcms.com/default-passwords-list'
    data = requests.get(url).text
    soup = BeautifulSoup.BeautifulSoup(data)
    table = soup.find("table",{'class':'tableizer-table'})
    for row in table.findAll('tr')[1:]: # skip th
        cells = row.findAll('td')
        username = cells[2].text
        password = cells[3].text
        line = username + separator + password
        for el in rpllist:
            line = line.replace(el,rpllist[el])
        add = 1
        for el in passlist:
            if line.find(el) >= 0:
                add = 0
        if add == 1:
            pwd_list[line] +=1

def get_cirtnet_list():
    url = 'http://cirt.net/passwords'
    data = requests.get(url).text
    soup = BeautifulSoup.BeautifulSoup(data)
    vendors = []
    links = soup.findAll('a')
    for link in soup.findAll('a'):
        if link['href'].find('?vendor=')>= 0:
            vendors.append('http://cirt.net/passwords'+link['href'])
    for link in vendors:
        data = requests.get(link).text
        soup = BeautifulSoup.BeautifulSoup(data)
        for table in soup.findAll('table', {'width':'95%'}):
            username = password = ''
            for row in table.findAll('tr'):
                cells = row.findAll('td')
                if cells[0].text == 'User ID':
                    username = cells[1].text
                if cells[0].text == 'Password':
                    password = cells[1].text
            line = username + separator + password
            for el in rpllist:
                line = line.replace(el,rpllist[el])
            add = 1
            for el in passlist:
                if line.find(el) >= 0:
                    add = 0
            if add == 1:
                pwd_list[line] +=1



if __name__ == '__main__':
    import argparse
    import operator
    desc = 'Download and create latest default password lists from multile repositories'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-s','--separator', help='Use the following char as separator, you probably want space which is default or TAB',type=str, default=' ')
    parser.add_argument('-n','--numbers', help='Print the list and use TABTAB as separator to print out occurance count (useful for statistics)', action="store_true")
    parser.add_argument('OUTPUT_FILE', help='The output file with your password list')
    args=parser.parse_args()
    wlfile = open(args.OUTPUT_FILE,'w')
    if args.separator == 'TAB':
        separator = '\t'
    else:
        separator = args.separator
    try:
        print '[+] Downloading and processing list: Phenoelit'
        get_phenoelit_list()
    except:
        print '[!] Error downloading Phenoelit list'
    try:
        print '[+] Downloading and processing list: LiquidMatrix'
        get_liquidmatrix_list()
    except:
        print '[!] Error downloading Liquidmatrix list'
    try:
        print '[+] Downloading and processing list: SecurityOverride'
        get_securityoverride_list()
    except:
        print '[!] Error downloading SecurityOverride list'
    try:
        print '[+] Downloading and processing list: DexCMS'
        get_dexcms_list()
    except:
        print '[!] Error downloading dexcms list'
    try:
        print '[+] Downloading and processing list: CirtNet'
        get_cirtnet_list()
    except:
        print '[!] Error downloading CirtNet list'
    print '[+] Sorting by occurance'
    sorted_wl = sorted(pwd_list.iteritems(), key=operator.itemgetter(1),reverse=True)
    print '[+] Dumping lists to file' 
    for el in sorted_wl:
        if args.numbers:
            wlfile.write( el[0].encode('utf-8')+'\t\t'+str(el[1])+'\n')
        else:
            wlfile.write( el[0].encode('utf-8') + '\n' )
    print '[+] Done!'
    wlfile.close()
