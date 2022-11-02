import redis


def connection(creds_file):
    with open(creds_file, 'r') as cf:
        creds = cf.read().split("\n")
        red = redis.Redis(host=creds[0],
                          port=creds[1],
                          password=creds[2])
        return red


def add(red, name, key):
    a = name.split(" ")
    var = a[0][0:4:1]+a[1][0:3:1]
    red.set(var, key)
