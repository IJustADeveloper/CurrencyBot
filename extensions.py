import redis
import requests
import json
import lxml.html


class BaseConn:
    def __init__(self, creds_file):
        self.conn = None
        self.connection(creds_file)

    def connection(self, creds_file):
        with open(creds_file, 'r') as cf:
            creds = cf.read().split("\n")
            self.conn = redis.Redis(host=creds[0],
                                    port=creds[1],
                                    password=creds[2])

    def add(self, name, val):
        a = name.split(" ")
        if len(a) > 1:
            var = a[0][0:3:1] + a[1][0:3:1]
        else:
            var = a[0][0:3:1]
        self.conn.set(var, val)

    def get_code(self, name):
        a = name.split(" ")
        if len(a) > 1:
            var = a[0][0:3:1] + a[1][0:3:1]
        else:
            var = a[0][0:3:1]
        return self.conn.get(var)

    def get_name(self, code):
        return self.conn.get(code).decode("utf-8")


class Parcer:
    @staticmethod
    def parce():
        r = requests.get("https://cdn.cur.su/api/cbr.json").content
        j = json.loads(r)

        return j

    @staticmethod
    def get_price(base, quote, amount):
        j = Parcer.parce()
        total = (float(amount) / float(j["rates"][base])) * float(j["rates"][quote])
        return total

    # трогать на свой страх и риск(без ее запуска и бд ничего работать не будет)
    # достает коды и наименования валют и сохраняет их в бд
    @staticmethod
    def parce_name():
        red = BaseConn("creds_file")
        r = requests.get("https://classifikators.ru/okv?ysclid=la0o3dyrsm210453020").content
        tree = lxml.html.document_fromstring(r)
        table = tree.xpath('/html/body/div[1]/div/main/div[4]/div[1]/div[1]/table/tbody')[0]
        try:
            for i in table:
                if len(i) >= 4:
                    var = i[2].text
                    val = i[3].text
                    red.add(red, var, val)
        except IndexError:
            pass
