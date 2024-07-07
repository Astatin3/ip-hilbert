with open("./ips_1.txt") as f:
    lines = f.readlines()
    for line in lines:
        print(line.split("/")[1].split(":")[0].rstrip())