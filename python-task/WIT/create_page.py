import re

from get_page import parse_page


def create(station):
    """
    генерация страницы для запроса
    :param station: объект "Станция"
    """
    with open("res\\template.html") as ex:
        template = ex.readlines()
        coord = station.img
        tran = station.trans
        l = len(coord)
        for i in range(l-1):
            desc = str(tran[i][0])
            template.insert(32 + i, "\tadd_marker({0},{1},'{2}',{3},map)\n"
                            .format(coord[i][0], coord[i][1], desc, 'i_tran'))

        template.insert(32, "\tadd_marker({0},{1},'{2}',{3},map)\n"
                        .format(coord[l-1][0], coord[l-1][1], ' ', 'i_stat'))
        # print(template[22])
        template[22] = template[22].replace('z', str(coord[l-1][0]))
        template[22] = template[22].replace('x', str(coord[l-1][1]))

        # print(station.page)
        num = re.search(r'\d+', station.page).group(0)
        # num = re.match(r'(\d+)', station.page).group(1)
        out = open('var\\station{}.html'.format(num), 'w')
        for i in template:
                out.write(i)
        out.close()


if __name__ == "__main__":
    s = "http://online.ettu.ru/station/1169"
    create(parse_page(s))