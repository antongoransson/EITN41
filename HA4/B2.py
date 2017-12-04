import requests
from sys import argv
requests.packages.urllib3.disable_warnings()

def get_req(url, payload):
     return requests.get(url, params=payload, verify=False)

def max_val(d):
    return max(d, key = d.get)

# https://eitn41.eit.lth.se:3119/ha4/addgrade.php?name=Kalle&grade=5&signature=6823
def brute_force(name, grade, h_str="0123456789abcdef", length=20, nbr_of_hits=2):
    url = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php"
    sign = "" #6823ea50b133c58cba36
    payload = {"name": name, "grade": grade, "signature": sign}
    while len(sign) < length:
        m_counts, hits = {}, False
        while not hits:
            req_times = {}
            for char in h_str:
                t_sign = sign + char
                payload["signature"] = t_sign
                req_times[t_sign] = get_req(url, payload).elapsed.total_seconds()
            s = max_val(req_times)
            try: m_counts[s] += 1
            except: m_counts[s] = 1
            hits = m_counts[s] == nbr_of_hits
        sign = s
    payload["signature"] = sign
    req = get_req(url, payload)
    ver = req.text.strip() == "1"
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
    brute_force(name, grade)
