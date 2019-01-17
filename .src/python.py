import sys
import socket
import ipaddress
import json


def get_ip():
    length = len(sys.argv)
    if length == 1:
        print("No argument was given, getting address...")
        address = socket.gethostbyname(socket.gethostname()) + "/24"
    elif length == 2:
        address = sys.argv[1]
        validate_ip(address)
        address = address + "/24"
    elif length == 3:
        address = sys.argv[1]
        validate_ip(address)
        mask = sys.argv[2]
        validate_mask(mask)
        address = address + "/" + mask
    else:
        exit("Invalid number of arguments!")
    return address


def validate_ip(address):
    split_address = address.split('.')
    if len(split_address) != 4:
        exit("Invalid address!")
    for x in split_address:
        if not x.isdigit():
            exit("Invalid address!")
        i = int(x)
        if i < 0 or i > 255:
            exit("Invalid address!")


def validate_mask(mask):
    for x in mask:
        if not x.isdigit():
            exit("Invalid mask!")
    if int(mask) < 0 or int(mask) > 31:
        exit("Invalid mask!")


def get_network(address):
    interface = ipaddress.IPv4Interface(address)
    print("Address: {0}".format(interface.network))
    return interface.network


def get_class(address):
    class_A = ipaddress.IPv4Network(("10.0.0.0", "255.0.0.0"))
    class_B = ipaddress.IPv4Network(("172.16.0.0", "255.240.0.0"))
    class_C = ipaddress.IPv4Network(("192.168.0.0", "255.255.0.0"))
    interface = ipaddress.IPv4Interface(address)

    if interface.ip in class_A:
        network_class = "A"
    elif interface.ip in class_B:
        network_class = "B"
    elif interface.ip in class_C:
        network_class = "C"
    else:
        network_class = "Not specified"
    print("Network Class: {0}".format(network_class))
    return network_class


def get_mask_decimal(address):
    interface = ipaddress.IPv4Interface(address)
    print("Subnet mask decimal: {0}".format(interface.netmask))
    return interface.netmask


def get_mask_binary(address):
    interface = ipaddress.IPv4Interface(address)
    temp = ip_to_bin(str(interface.netmask))
    print("Subnet mask binary: {0}".format(temp))
    return temp


def get_broadcast_decimal(address):
    interface = ipaddress.IPv4Interface(address)
    print("Broadcast decimal: {0}".format(interface.network.broadcast_address))
    return interface.network.broadcast_address


def get_broadcast_binary(address):
    interface = ipaddress.IPv4Interface(address)
    temp = ip_to_bin(str(interface.network.broadcast_address))
    print("Broadcast binary: {0}".format(temp))
    return temp


def get_host_min_decimal(address):
    net = ipaddress.IPv4Interface(address)
    temp = next(net.network.hosts())
    print("HostMin decimal: {0}".format(temp))
    return temp


def get_host_min_binary(address):
    net = ipaddress.IPv4Interface(address)
    temp = ip_to_bin(str(next(net.network.hosts())))
    print("HostMin binary: {0}".format(temp))
    return temp


def get_host_max_decimal(address):
    net = ipaddress.IPv4Interface(address)
    temp = ""
    for x in net.network.hosts():
        temp = x
    print("HostMax decimal: {0}".format(temp))
    return temp


def get_host_max_binary(address):
    net = ipaddress.IPv4Interface(address)
    temp = ""
    for x in net.network.hosts():
        temp = x
    temp = ip_to_bin(str(temp))
    print("HostMax binary: {0}".format(temp))
    return temp


def get_max_hosts_number_decimal(address):
    net = ipaddress.IPv4Interface(address)
    counter = 0
    for x in net.network.hosts():
        counter += 1
    print("Max number of hosts decimal: {0}".format(counter))
    return bin(counter)


def get_max_hosts_number_binary(address):
    net = ipaddress.IPv4Interface(address)
    counter = 0
    for x in net.network.hosts():
        counter += 1
    print("Max number of hosts binary: {0}".format("{0:b}".format(counter)))
    return counter


def ip_to_bin(address):
    temp = address.split('.')
    address = ""
    y = 0
    for x in temp:
        i = int(x)
        x = "{0:b}".format(i)
        temp[y] = x
        y = y + 1
    for i in range(0, 3):
        address += temp[i]
        address += "."
    address += temp[3]
    return address


def main():
    address = get_ip()

    data = {'Calculator': []}
    data['Calculator'].append({'Address': str(get_network(address))})
    data['Calculator'].append({'Network Class': get_class(address)})
    data['Calculator'].append({'Subnet mask decimal': str(get_mask_decimal(address)),
                               'Subnet mask binary': str(get_mask_binary(address))})
    data['Calculator'].append({'Broadcast decimal': str(get_broadcast_decimal(address)),
                               'Broadcast binary': str(get_broadcast_binary(address))})
    data['Calculator'].append({'HostMin decimal': str(get_host_min_decimal(address)),
                               'HostMin binary': str(get_host_min_binary(address))})
    data['Calculator'].append({'HostMax decimal': str(get_host_max_decimal(address)),
                               'HostMax binary': str(get_host_max_binary(address))})
    data['Calculator'].append({'Max number of hosts decimal': get_max_hosts_number_decimal(address),
                               'Max number of hosts binary': get_max_hosts_number_binary(address)})

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)


if __name__ == '__main__':
    main()
