# Copyright (c) 2014 Gergely Imreh gergely@imreh.net

# Most of this code came from Gergely Imreh on GitHub: https://github.com/imrehg/mailcount
# I adapted his program to work with Python3 to use in my project

#!/usr/bin/env python3
"""
Scripot
"""
from datetime import date, timedelta
import datetime
import email
import imaplib
import sys
import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


DEBUG = False  # whether to do extra progress printing

if len(sys.argv) < 2:
    filename = os.path.basename(__file__)
    print("Usage: %s <configfile>" %filename)
    sys.exit(1)

configfile = sys.argv[1]
if not os.path.isfile(configfile):
    print("Error: can't find config file at '%s'" %(configfile))
    sys.exit(1)

config = configparser.ConfigParser()
config.read(configfile)

accounts = []
for section in config.sections():
    if section == 'Options':
        continue
    try:
        mail = { 'name': section,
                 'server': config.get(section, 'server'),
                 'login': config.get(section, 'login'),
                 'pass': config.get(section, 'pass'),
                 'mailbox': config.get(section, 'mailbox'),
             }
    except:
        raise
    accounts += [mail]


offset = 1  # Today=0, Yesterday=1, 2-days-ago=2,...
finish_date = date.today() + timedelta(1 - offset)
start_date = date.today() - timedelta(offset)

finish_date_str = finish_date.strftime("%d-%b-%Y")
start_date_str = start_date.strftime("%d-%b-%Y")

# Print date of query for clarity
if offset == 0:
    offset_string = "today"
elif offset == 1:
    offset_string = "yesterday"
else:
    offset_string = "%d days ago" %(offset)
print("Query time: %s (%s)" %(start_date_str, offset_string) )

if DEBUG:
    print("From %s to %s" %(start_date_str, finish_date_str))

def process_mailbox(M):
    """ Count the number of messages according to the global settings
    and return the number of mesages within the given time period
    """
    query = '(SINCE "%s" BEFORE "%s")' %(start_date_str, finish_date_str)
    rv, data = M.search(None, query)
    if rv != 'OK':
        return 0

    count = len(data[0].split())

    if DEBUG:
        for num in data[0].split():
            rv, data = M.fetch(num, '(RFC822)')
            if rv != 'OK':
                print("ERROR getting message", num)
                return

            msg = email.message_from_string(data[0][1].decode('utf-8'))
            print('Message %s: %s' % (num, msg['Subject']))
            print('Raw Date:', msg['Date'])
            date_tuple = email.utils.parsedate_tz(msg['Date'])
            if date_tuple:
                local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                print("Local Date: %s" %(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
    # store date with some type of counter
    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_string(data[0][1].decode('utf-8'))
        # print('Message %s: %s' % (num, msg['Subject']))
        # print('Raw Date:', msg['Date'])
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            print("Local Date: %s" %(local_date.strftime("%H:%M:%S")))
    return count

def getsent(account):
    M = imaplib.IMAP4_SSL(account['server'])
    try:
        M.login(account['login'], account['pass'])
    except imaplib.IMAP4.error:
        print("LOGIN FAILED!!! ")
        return 0

    if DEBUG:
        mboxes = M.list()
        for m in mboxes:
            print(m)

    total = 0
    rv, data = M.select(account['mailbox'])
    if rv == 'OK':
        if DEBUG:
            print("Processing mailbox...\n")
        total = process_mailbox(M)
        M.close()
    M.logout()
    return total

total = 0
for a in accounts:
    val = getsent(a)
    print("%s: %d" %(a['name'], val))
    total += val

print("-"*20)
print("Total emails: %d" %(total))
