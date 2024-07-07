def inverse_hilbert_xy(x, y, order=16):
    """Convert (x, y) on a Hilbert curve of given order to IP integer."""
    ip_int = 0
    for i in range(order - 1, -1, -1):
        xi = (x >> i) & 1
        yi = (y >> i) & 1

        if yi == 0:
            if xi == 1:
                x, y = (1 << order) - 1 - y, (1 << order) - 1 - x
            x, y = y, x

        ip_int |= (xi << (2 * i)) | (yi << (2 * i + 1))

    return ip_int


def ip_int_to_ip(ip_int):
    """Convert an integer IP address to a string IP address."""
    return ".".join(str((ip_int >> i) & 0xFF) for i in [24, 16, 8, 0])

def generate_ip_ranges(size=16, order=16):
    # for x in range(size):
    #     for y in range(size):
    #         x_pos = int((x/size)*(2 ** order)/2)
    #         y_pos = int((y/size)*(2 ** order)/2)
    #         ip = inverse_hilbert_xy(x_pos, y_pos, order=order)
    #         print(ip_int_to_ip(ip))

    for x in range(256):
        for y in range(256):
            print(str(x)+"."+str(y)+".255.255")



if __name__ == "__main__":
    generate_ip_ranges()