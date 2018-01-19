#!/usr/bin/env python3
__author__ = 'kowalski'
import sys
import re

if len(sys.argv) == 1 or sys.argv[1] == '-h':
    print('Hi! Arguments for programme:')
    print('1) -u -- search the most popular browser')
    print('2) -b -- calculating bytes in day')
    print('Ex.: ./classes.py -u file')
    sys.exit(0)

if len(sys.argv) > 2:
    try:
        file = open(sys.argv[2], 'r')
    except IOError as error:
        print('IOError: {}'.format(error))
        sys.exit(0)
else:
    print('Please write a correct filename')
    sys.exit(0)


class LogParser:
    browser = ''
    days = {}

    def __init__(self, type_p, file_in):
        if type_p == '-u':
            browsers = {}
            self.search_brow(file_in, browsers)
            self.browser = self.find_pop(browsers)
            print(self.edit_name(self.browser) + ': ' + str(browsers[
                  self.browser]))
        elif type_p == '-b':
            self.calc_bytes(file_in, self.days)
            for i in self.days:
                print(str(i) + ': ' + str(self.days[i]))

    @staticmethod
    def search_brow(file_in, browsers):
        reg_pars = re.compile('\[([0-9]{,2}/[a-zA-Z]+/[0-9]{,4}).*]'
                              '.*?".*?" "(.*?)" ([0-9]*)')
        for line in file_in:
            res = reg_pars.findall(line)
            if len(res) > 0:
                if res[0][1] in browsers:
                    browsers[res[0][1]] += 1
                else:
                    browsers[res[0][1]] = 1

    @staticmethod
    def find_pop(browsers):
        return max(browsers, key=browsers.get)

    @staticmethod
    def edit_name(name):
        if name.find('Firefox') or name.find('MSIE') or name.find('Chrome'):
            reg_brow = re.compile('.*?(MSIE [0-9.]+?|Firefox/[0-9.]+?'
                                  '|Chrome/[0-9.]+?)[;" ]')
            return reg_brow.findall(name)[0]
        elif name.find('Opera'):
            reg_brow = re.compile('.*?(Version/[0-9.]+?)[;" ]')
            return 'Opera ' + reg_brow.match(name).group(1)

    @staticmethod
    def calc_bytes(file_in, days):
        reg_pars = re.compile('\[([0-9]{,2}/[a-zA-Z]+/[0-9]{,4}).*]'
                              '.*?".*?" "(.*?)" ([0-9]*)')
        for line in file_in:
            res = reg_pars.findall(line)
            if len(res) > 0:
                if res[0][0] in days:
                    days[res[0][0]] += int(res[0][2])
                else:
                    days[res[0][0]] = int(res[0][2])

LogParser(sys.argv[1], file)
file.close()
