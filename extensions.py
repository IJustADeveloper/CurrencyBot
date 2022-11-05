import redis
import requests
import json
import lxml.html


class BaseConn:
    def __init__(self, host, port, password):
        self.conn = None
        self.connection(host, port, password)

    def connection(self, host, port, password):
        self.conn = redis.Redis(host=host,
                                port=port,
                                password=password)

    def add(self, name, val):
        a = name.split(" ")
        if len(a) > 1:
            var = a[0][0:3:1] + a[1][0:3:1]
        else:
            var = a[0][0:3:1]
        self.conn.set(var, val)

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
        if base == quote:
            raise QueryException(f"Невозможно перевести одинаковые валюты {base}")
        try:
            b_code = j["rates"][base.upper()]
        except KeyError:
            raise QueryException(f"Валюта {base} не существует. Проверьте написание.")
        try:
            q_code = j["rates"][quote.upper()]
        except KeyError:
            raise QueryException(f"Валюта {quote} не существует. Проверьте написание.")
        try:
            amount = float(amount)
        except ValueError:
            raise QueryException(f"Неверный ввод количетсва переводимой валюты.")
        total = (amount / float(b_code) * float(q_code))
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


class QueryException(Exception):
    def __init__(self, message):
        super().__init__(message)
