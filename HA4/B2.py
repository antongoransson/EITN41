import requests
requests.packages.urllib3.disable_warnings()

# https://eitn41.eit.lth.se:3119/ha4/addgrade.php?name=Kalle&grade=5&signature=6823
def brute_force(name, grade, string="0123456789abcdef", length=20):
    sign = "" #6823ea50b133c58cba36
    url = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php?"
    payload = {"name": name, "grade": grade, "signature": sign}
    ver = False
    while not(ver):
        while len(sign) < length:
            req_times = {}
            for char in string:
                try_sign = sign + char
                payload["signature"] = try_sign
                req = requests.get(url, params=payload, verify=False)
                req_times[try_sign] = req.elapsed.total_seconds()
            sign = max(req_times, key = req_times.get)
        payload["signature"] = sign
        r = requests.get(url, params=payload, verify=False)
        ver = r.text.strip() == "1"
    print("Request: ?name={}&grade={}&signature={}".format(name, grade, sign))
    print("Signature valid: {}".format(r.text.strip() == "1"))
    print("Name: {}, Grade: {}, Signature: {}".format(name, grade, sign))
    return sign

if __name__ == '__main__':
    sign=""
    brute_force("Jonathan", 3)
    brute_force("Kalle", 5)
