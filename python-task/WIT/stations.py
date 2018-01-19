__author__ = 'Антон'
import urllib.request
import re
from bs4 import BeautifulSoup


def get_stations(page):
    """
    получение всех остановок
    :param page: адрес сайта ЕМУП
    :return: два листа результатов
    """
    source = urllib.request.urlopen(page)
    s = source.read()
    soup = BeautifulSoup(s)
    links = soup.find_all(href=re.compile('station'))
    stations = []
    reg = re.compile('href="(/\w+/(%*[A-Z0-9]*)*)">(.*)</a>')
    for i in links:
        l = reg.findall(i.decode())[0][0]
        stations.append(page + str(l))
    tramm = []
    troll = []
    for i in stations:
        t1, t2 = get_stations_from_page(i)
        for j in t1:
            tramm.append(j)
        for j in t2:
            troll.append(j)
    return tramm, troll


def get_stations_from_page(page):
    """
    получение адреса страницы остановки и ее название со страницы выбора
    :param page: страница
    :return: два листа результатов по двум разным типам транспорта
    """
    source = urllib.request.urlopen(page)

    s = source.read()
    soup = BeautifulSoup(s)
    l = soup.findAll('div')
    dat = re.findall('<h3>(.*)</h3>\n((<a href=".*".*\n)*)', l[0].decode())
    reg = re.compile('href="(.*)">(.*)</a>')
    # Некоторые страницы имеют информацию или только о трамваях, или только
    # о троллейбусах. Если такая страница находиться, будет выполняться
    # тернарный оператор
    if len(dat) > 1:
        tramm = reg.findall(dat[0][1])
        tramm = [(page[:21] + i[0], i[1]) for i in tramm]
        troll = reg.findall(dat[1][1])
        troll = [(page[:21] + i[0], i[1]) for i in troll]
    else:
        temp = reg.findall(dat[0][1])
        tramm, troll =\
            [([(page[:21] + i[0], i[1]) for i in temp], []),
             ([], [(page[:21] + i[0], i[1]) for i in temp])][dat[0][0] ==
                                                             "Трамваи"]
    return tramm, troll

if __name__ == "__main__":
    site = "http://online.ettu.ru"
    t1, t2 = get_stations(site)
    print(t1)
    print(t2)
