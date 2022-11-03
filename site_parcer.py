import requests
import lxml.html
import json
from extensions import BaseConn


def parce():
    r = requests.get("https://cdn.cur.su/api/cbr.json").content
    j = json.loads(r)

    return j


# собирает коды и названия валюты в БД
def parce_name():
    red = BaseConn("creds_file")
    r = requests.get("https://classifikators.ru/okv?ysclid=la0o3dyrsm210453020").content
    tree = lxml.html.document_fromstring(r)
    table = tree.xpath('/html/body/div[1]/div/main/div[4]/div[1]/div[1]/table/tbody')[0]
    try:
        for i in table:
            if len(i)>=4:
                var = i[3].text
                val = i[2].text
                red.add(red, val, var)
    except IndexError:
        pass
