__author__ = 'Антон'
import urllib.request
import urllib.parse
import re

from bs4 import BeautifulSoup
import CStation


def parse_page(page):
    """
    Разбирает страницу остановки
    :param page: адрес страницы остановки
    :return: Объект "станиция", хранящий всю информацию о транспорте
    """
    source = urllib.request.urlopen(page)
    site = source.read()
    soup = BeautifulSoup(site)
    # узнаем из второго заголовка тип остановки
    title = soup.h2.find_all(href=re.compile('/m/Main'))
    title = re.findall('>\s*([а-яА-Я]*\s[а-яА-Я]*)', title[0].decode())[0]
    typ = 0
    if title == "Где трамвай":
        typ = 0
    else:
        typ = 1
    # получение номер, время и растояние
    # до остановки транспорта ввиде листа таплов
    p = soup.div
    tran = re.findall('>(<b>)?(.*?)(</b>)?</div>', p.decode())
    tran = [i[1] for i in tran]
    tran = [tuple(tran[i:i+3]) for i in range(0, len(tran), 3)]
    # получение координат транспорта
    try:
        img = soup.img.decode()
        # если мы не можем получить коориднаты,
        # предыдущая строка пытается декодировать None
    except AttributeError:
        img = []
    else:
        img = re.findall('src="(.*)"/>', img)[0]
        s = ''
        t = img.split('amp;')
        for i in t:
            s += i
        img = s
        f = re.findall('(\d+.\d+,\d+.\d+)', img)
        img = tuple((float(f[i].split(',')[0]), float(f[i].split(',')[1]))
                    for i in range(len(f) // 2))

    return CStation.Station(typ, tran, img, page)


if __name__ == "__main__":
    site_t = "http://online.ettu.ru/station/3497"
    site = "http://online.ettu.ru/station/962946"
    s = "http://online.ettu.ru/station/962064"
    print(parse_page(site_t))
    print(parse_page(site))
    print(parse_page(s))
