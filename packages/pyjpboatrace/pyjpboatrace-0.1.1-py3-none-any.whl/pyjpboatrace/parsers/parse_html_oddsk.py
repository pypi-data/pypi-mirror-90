from bs4 import BeautifulSoup
from pyjpboatrace.utils import str2num


def parse_html_oddsk(html: str):

    def parse_quinellaplace(trs):

        dic = {}
        for i, tr in enumerate(trs):
            tds = tr.select('td')
            b2 = i + 2
            for j, (tdo, tde) in enumerate(zip(tds[::2], tds[1::2])):
                b1 = j + 1
                if b1 >= b2:  # invalid quinella-place
                    break
                dic[f'{b1}={b2}'] = list(map(
                    lambda s: str2num(s, float, s),
                    tde.text.split('-')
                ))

        return dic

    # make soup
    soup = BeautifulSoup(html, 'html.parser')

    # table
    tables = soup.select('div.table1')  # probably 2 tables
    quinellaplace_table = tables[-1].select('table > tbody > tr')

    # parse
    dic = parse_quinellaplace(quinellaplace_table)

    return dic
