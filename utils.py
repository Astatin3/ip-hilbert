# https://github.com/bonsaiviking/IPMap/blob/master/ipmap/hilbert.py
def xy2d(side_length: int, x: int, y: int):
    """Find the distance of the point (x, y) along a Hilbert curve
    which fills a square *side_length* units on a side."""
    y = side_length-y
    s = side_length / 2
    d = 0
    while( s > 0 ):
        rx = 1 if (int(x) & int(s)) else 0
        ry = 1 if (int(y) & int(s)) else 0
        d += s * s * ((3 * rx) ^ ry)
        if (ry == 0):
            if (rx == 1):
                x = s-1 - x
                y = s-1 - y
            (x, y) = (y, x)
        s /= 2
    return int(d)

# https://github.com/bonsaiviking/IPMap/blob/master/ipmap/hilbert.py
def d2xy(side_length: int, d: int):
    """Find the coordinates (x, y) of a point some distance *d* along
    a Hilbert curve which fills a square *side_length* units on a side."""
    x = y = 0
    s = 1
    while( s < side_length ):
        rx = 1 & int(d/2)
        ry = 1 & (int(d) ^ rx)
        if (ry == 0):
            if (rx == 1):
                x = s-1 - x
                y = s-1 - y
            (x, y) = (y, x)
        x += s * rx
        y += s * ry
        d /= 4
        s *= 2

    # if y < 10000:
    #     print(ip_int_to_ip(int(d)))

    return x, side_length-y

def ip_to_int(ip):
    return int(''.join([bin(int(x) + 256)[3:] for x in ip.split('.')]), 2)

def ip_int_to_ip(ip_int):
    return ".".join(str((ip_int >> i) & 0xFF) for i in [24, 16, 8, 0])


def ipInCIDR(ip: str, ip_CIDR: str):
    range_parts = ip_CIDR.split('/')
    range_mask = int(range_parts[1])

    range_mask_num = (0xFFFFFFFF << (32 - range_mask)) & 0xFFFFFFFF

    return (ip_to_int(ip) & range_mask_num) == (ip_to_int(range_parts[0]) & range_mask_num)


def ipInRange(ip: str, ip_range: str):
    ip_int = ip_to_int(ip)
    start_ip_int, end_ip_int = [ip_to_int(ip) for ip in ip_range.split('-')]

    return start_ip_int <= ip_int <= end_ip_int

reserved_ip_blocks=[
    "0.0.0.0/8",
    "10.0.0.0/8",
    "100.64.0.0/10",
    "127.0.0.0/8",
    "169.254.0.0/16",
    "172.16.0.0/12",
    "192.0.0.0/24",
    "192.0.2.0/24",
    "192.88.99.0/24",
    "192.168.0.0/16",
    "198.18.0.0/15",
    "198.51.100.0/24",
    "203.0.113.0/24",
    "224.0.0.0/4",
    "233.252.0.0/24",
    "240.0.0.0/4",
    "255.255.255.255/32"
]

def is_valid_ip(ip: str):
    if ":" in ip:
        ip = ip.split(":")[0]

    for reserved_ip in reserved_ip_blocks:
        if ipInCIDR(ip, reserved_ip):
            return False
    return True
