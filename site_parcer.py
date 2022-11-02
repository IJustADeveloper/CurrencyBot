import requests
import lxml.html
import json
from db_connect import connection, add

def parce():
    r = requests.get("https://cdn.cur.su/api/cbr.json").content
    j = json.loads(r)

    return j


def parce_name():
    red = connection("creds_file")
    r = requests.get("http://www.consultant.ru/document/cons_doc_LAW_31966/5ebb56e60f3126b262bd44c2e7d258fea7179649/?ysclid=l9zo9ybw5y268320860").content
    tree = lxml.html.document_fromstring(r)
    table = tree.xpath('/html/body/div/section/div[1]/div[1]/div[3]/div[2]/table')
    var = 0
    key = 0
    for i in range(len(table[0])):
        if len(table[0][i])>3:
            if len(table[0][i][1][0])==0:
                print(len(table[0][i]), table[0][i][1][0].text)
            else:
                print(len(table[0][i]), table[0][i][1][0][0])
        '''if len(table[0][i])==4:
            var = table[0][i]
            key = table[0][i]
        print(var, key)'''

print(parce_name())
