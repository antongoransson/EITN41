from converter import *
from pcapfile import savefile
from ipaddress import IPv4Address

def all_is_disjoint(R, R_other):
    return all([R_i.isdisjoint(R_other) for R_i in R])

def learning_phase(sender_ip, mix_ip, m, file_in):
    ip_sources, ip_dests = parse_pcap_file(file_in)
    R, R_other, i = [], [], 0
    while i is not None:
        i = ip_sources.index(sender_ip, i)
        start = i = ip_sources.index(mix_ip, i)
        try: i = ip_dests.index(mix_ip, i)
        except: i = None
        receivers = ip_dests[start:i]
        tmp_set = R if len(R) < m and all_is_disjoint(R, receivers) else R_other
        tmp_set.append(set(receivers))
    return R, R_other

def excluding_phase(R, R_other):
    for item_set in R_other:
        disjoint_sets = [i for i in range(len(R)) if not(R[i].isdisjoint(item_set))]
        if len(disjoint_sets) == 1:
            R[disjoint_sets[0]] &= item_set
    return R

def find_partners(sender_ip, mix_ip, m, file_in):
    R, R_other = learning_phase(sender_ip, mix_ip, m, file_in)
    partners = excluding_phase(R, R_other)
    ip_sum = get_ip_sum(partners)
    return ip_sum

def get_ip_sum(R):
    ip_ints = [int(IPv4Address(next(iter(item_set)))) for item_set in R]
    return sum(ip_ints)


def parse_pcap_file(file_in):
    testcap = open(file_in, 'rb')
    capfile = savefile.load_savefile(testcap, layers=2)
    ip_sources, ip_dests = [], []
    for pkt in capfile.packets:
        ip_sources.append(pkt.packet.payload.src.decode('UTF8'))
        ip_dests.append(pkt.packet.payload.dst.decode('UTF8'))
    testcap.close()
    return ip_sources, ip_dests

if __name__ == '__main__':
    print(find_partners('159.237.13.37', '94.147.150.188', 2, 'inputs/B2_cia.log.1337.pcap'))
    print(find_partners("161.53.13.37", "11.192.206.171", 12, 'inputs/B2_cia.log.1339.pcap'))
