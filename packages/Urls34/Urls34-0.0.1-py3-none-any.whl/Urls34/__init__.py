import urllib.request
import requests


def urlread(url, file=None, *, file_name="Read Url"):
    rl = urllib.request.urlopen(url)
    if file == None:
        return rl.read()
    if file == True:
        f = open(file_name, "wb")
        f.write(rl.read())
    if file == False:
        return rl.read()


def get_response(url):
    res = requests.get(url)
    return res


def contact_api(url):
    res = requests.get(url)
    r = res.json()
    return r