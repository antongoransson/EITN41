import requests

# https://eitn41.eit.lth.se:3119/ha4/addgrade.php?name=Kalle&grade=5&signature=6823...ba36
def brute_force(name, grade):
    sig = "" #6823ea50b133c58cba36
    requests.packages.urllib3.disable_warnings()
    url = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php?"
    string = "0123456789abcdef"
    while len(sig) < 20:
        times = {}
        for char in string:
            R = sig + char
            payload = {'name': name, 'grade': grade, 'signature':R}
            r = requests.get(url, params=payload, verify=False)
            r_time = r.elapsed.total_seconds()
            times[R] = r_time
        sig = max(times, key = times.get)#keywithmaxval(times)
    payload = {'name': name, 'grade': grade, 'signature': sig}
    r = requests.get(url, params=payload, verify=False)
    print(r.text)
    print(sig)

brute_force("Kalle", 5)
