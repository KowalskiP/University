#!/usr/bin/env python3
__author__ = 'kowalski'
import sys
if len(sys.argv) > 2:
    print('You wrote a wrong param')
    sys.exit(0)

import re
from urllib.request import urlopen, url2pathname, pathname2url
reg = re.compile('<a href="/wiki/([A-Z0-9_%]*?)" title="[^/\[\]A-Za-z]*?"')
philosophy = '%D0%A4%D0%B8%D0%BB%D0%BE%D1%81%D0%BE%D1%84%D0%B8%D1%8F'


class Page:
    def __init__(self, url, prev):
        self.url = url
        self.prev = prev


def open_page(dom, url):
    return urlopen(dom + url).read().decode()


def get_urls(page):
    return reg.findall(page)


def control(link, lst):
    for l in lst:
        if link == l.url:
            return True


def create_pages(source, lst, begin):
    for s in source:
        if not control(s, lst):
            lst.append(Page(s, begin))
    return lst


def search_phil(lst):
    for l in lst:
        if l == philosophy:
            return True


def path(source, res=''):
    if source:
        res = url2pathname(source.url) + '>>' + res
        path(source.prev, res)
    else:
        res += url2pathname(philosophy)
        print(res)

domain = 'http://ru.wikipedia.org/wiki/'
source_url = sys.argv[1]
source_page = urlopen(domain + pathname2url(source_url)).read().decode()
source_urls = get_urls(source_page)
urls = []
create_pages(source_urls, urls, Page(source_url, None))

if search_phil(source_urls):
    print(source_url + '>>' + url2pathname(philosophy))
    sys.exit(0)

for i in urls:
    new = urlopen(domain + i.url).read().decode()
    new_urls = get_urls(new)
    if search_phil(new_urls):
        path(i)
        sys.exit(0)
    for u in new_urls:
        if not control(u, urls):
            urls.append(Page(u, i))
