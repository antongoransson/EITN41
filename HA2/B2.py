from converter import *
from pcapfile import savefile

def learning_phase(sender_ip, mix_ip, m, file_in):
    ip_sources, ip_dests = parse_pcap_file(file_in)
    length = len(ip_sources)
    R, sets = [], []
    i = 0
    while i < length:
        receivers = []
        if ip_sources[i] == sender_ip:
            while ip_sources[i] != mix_ip:
                 i += 1
            while i < length and ip_sources[i] == mix_ip:
                receivers.append(ip_dests[i])
                i += 1
            i -= 1 # Otherwise first sender after mix would be skipped
            if len(R) < m and is_disjoint(R, receivers): R.append(set(receivers))
            else: sets.append(set(receivers))
        i += 1
    return R, sets

def excluding_phase(R, sets):
    disjoint_sets = 0
    for item_set in sets:
        for i in range(len(R)):
            if not(R[i].isdisjoint(item_set)):
                disjoint_sets += 1
                index = i
        if disjoint_sets == 1:
            R[index] = R[index] & item_set
        disjoint_sets = 0
    return R

def find_partners(sender_ip, mix_ip, m, file_in):
    R, sets = learning_phase(sender_ip, mix_ip, m, file_in)
    partners = excluding_phase(R, sets)
    ip_sum = get_ip_sum(partners)
    return ip_sum

def get_ip_sum(R):
    ip_ints = [ip_to_int("".join(item_set)) for item_set in R]
    return sum(ip_ints)

def ip_to_int(ip):
    hex_str = [int_to_hex(int(ip))[2:].zfill(2) for ip in ip.split(".")]
    string = "0x" + "".join(hex_str)
    return hex_to_int(string)

def is_disjoint(list_of_sets, set2):
    for item_set in list_of_sets:
        if not(item_set.isdisjoint(set2)):
            return False
    return True

def parse_pcap_file(file_in):
    testcap = open(file_in, 'rb')
    capfile = savefile.load_savefile(testcap, layers=2)
    # print ('timestamp\t\teth src\t\t\teth dst\t\t\tIP src\t\tIP dst')
    ip_sources = []
    ip_dest = []
    for pkt in capfile.packets:
        ip_src = pkt.packet.payload.src.decode('UTF8')
        ip_sources.append(ip_src)
        ip_dst = pkt.packet.payload.dst.decode('UTF8')
        ip_dest.append(ip_dst)
        # print ('{}\t\t{}\t{}\t{}\t{}'.format(timestamp, eth_src, eth_dst, ip_src, ip_dst))
    testcap.close()
    return ip_sources, ip_dest
if __name__ == '__main__':
    print(find_partners('159.237.13.37', '94.147.150.188', 2, 'inputs/B2_cia.log.1337.pcap'))
    print(find_partners("161.53.13.37", "11.192.206.171", 12, 'inputs/B2_cia.log.1339.pcap'))
