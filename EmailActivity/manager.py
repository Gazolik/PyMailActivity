import sys
import os

import email

class Manager(object):

    def __init__(self, directory, date_format='%Y-%m-%d'):
        self.directory = directory
        self.files = [i for i in os.listdir(directory) if i[-4:] == '.eml']
        print('number of files ', len(self.files))
        self.format = date_format

        self.senders = {}
        self.receivers = {}
        self.sender_dates = {}
        self.receiver_dates = {}

    def weight(self, mail):
        ''' return the weight of a mail '''
        return 1

    def extract(self, message):
        ''' extract date, addresses in the field "from" and adresses in the field "to" of a message'''
        date = email.utils.parsedate_to_datetime(message['Date']).strftime(self.format)
        sender_list = parse_address(message['from'])
        receiver_list = parse_address(message['to'])
        return date, sender_list, receiver_list

    def increment_dict(self, dic, inc, weight):
        ''' increment a value in a dict if doesn't exist or instanciate it'''
        dic['tot'] += weight
        if inc in dic:
            dic[inc] += weight
        else:
            dic[inc] = weight


    def classify(self, mail):
        '''fill the manager fields with a mail'''
        m = ''
        with open(self.directory + '/' + mail, 'r', errors='ignore') as f:
            m = email.message_from_file(f)
        
        date, sender_list, receiver_list = self.extract(m)
        w = self.weight(m)
        
        if date not in self.sender_dates:
            self.sender_dates[date] = {'tot': 0}
        
        if date not in self.receiver_dates:
            self.receiver_dates[date] = {'tot': 0}
        

        for s in sender_list:
            self.increment_dict(self.sender_dates[date], s, w)
            if s not in self.senders:
                self.senders[s] = {'tot': 0}
            self.increment_dict(self.senders[s], date, w)
        
        for r in receiver_list:
            self.increment_dict(self.receiver_dates[date], s, w)
            if r not in self.receivers:
                self.receivers[r] = {'tot': 0}
            self.increment_dict(self.receivers[r], date, w)


    def process_all(self):
        '''process all mails in the mail folder'''

        tot = len(self.files)
        cpt = 0
        for mail in self.files:
            done=str(int((float(cpt)/tot)*100))
            sys.stdout.write("%s%%      %s"%(done,"\r"))
            sys.stdout.flush()
            self.classify(mail)
            cpt += 1



    def pprint(self):
        ''' ugly pretty print '''
        print(self.senders)
        print(self.receivers)
        print(self.sender_dates)
        print(self.receiver_dates)

def parse_address(field):
    ''' parse an address filed: split if several addresses, remove the <> and extract the domain name'''
    adresses_bad = field.split(',')
    adresses_good = []
    for a in adresses_bad:
        try:
            start = a.index('<')
            end = a.index('>')
            tmp = a[start+1:end]
            at = tmp.index('@') +1
            adresses_good.append(tmp[at:])
        except ValueError:
            continue
    return adresses_good


