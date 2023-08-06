from bs4 import BeautifulSoup
from pyjpboatrace.utils import str2num


def parse_html_odds2tf(html: str):

    def parse_exacta(trs):
        # preparation
        lst_tds = [tr.select('td') for tr in trs]
        # extract
        dic = {}
        for i, tds in enumerate(lst_tds):
            b2 = i + 2
            for j, tde in enumerate(tds[1::2]):
                b1 = j + 1
                dic[f'{b1}-{b2}'] = str2num(tde.text, float, tde.text)
                if i == j:  # upper right of table
                    b2 = b2 - 1

        return dic

    def parse_quinella(trs):
        # preparation
        lst_tds = [tr.select('td') for tr in trs]
        # extract
        dic = {}
        for i, tds in enumerate(lst_tds):
            b2 = i + 2
            for j, tde in enumerate(tds[1::2]):
                b1 = j + 1
                if b1 >= b2:  # invalid quinella
                    break
                dic[f'{b1}={b2}'] = str2num(tde.text, float, tde.text)

        return dic

    # make soup
    soup = BeautifulSoup(html, 'html.parser')

    # table
    tables = soup.select('div.table1')  # probably 3 tables
    exacta_table = tables[-2].select('table > tbody > tr')
    quinella_table = tables[-1].select('table > tbody > tr')

    # parse
    dic = {
        'exacta': parse_exacta(exacta_table),
        'quinella': parse_quinella(quinella_table),
    }

    return dic
