import os
import socket
from dns import resolver

def load_authorized_keys(user):
    import paramiko
    import base64
    authorized_keys = []
    try:
        with open(os.environ['DN42_REGISTRY_DIRECTORY'] + "/data/mntner/" + user.upper() + "-MNT", 'r') as file:
            for line in file:
                l = line.strip().split()
                if len(l) >= 3 and l[0] == 'auth:':
                    key_type = l[1]
                    key_data = l[2]
                    if key_type == 'ssh-ed25519':
                        key = paramiko.Ed25519Key(data=base64.b64decode(key_data))
                    elif key_type == 'ssh-rsa':
                        key = paramiko.RSAKey(data=base64.b64decode(key_data))
                    else:
                        continue
                    authorized_keys.append(key)
    except:
        pass
    return authorized_keys

def as_maintained_by(user):
    as_nums = []

    directory = os.environ['DN42_REGISTRY_DIRECTORY'] + "/data/aut-num"
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, "r") as file:
                for line in file:
                    l = line.strip().split()
                    if len(l) == 2 and l[0] == 'mnt-by:' and l[1] == user.upper() + "-MNT":
                        as_nums.append(filename[2:])
        except:
            pass

    return as_nums

def get_ipv6(host):
    try:
        socket.inet_pton(socket.AF_INET6, host)
        return [host]
    except:
        pass

    try:
        answers = resolver.resolve(host, 'AAAA')
        return [rdata.address for rdata in answers]
    except:
        return []

def peer_create(as_num, wg_pub_key, wg_end_point_addr, wg_end_point_port):
    return True

def get_peer_list():
    return ["4242420266", "4242420276"]
#    return ["4242420263", "4242420264"]

def peer_remove(as_num):
    return True

def peer_status(as_num=0):
    pass
