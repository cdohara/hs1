# n = base, m modulus, goal exponent
def fastexp(n, m, goal):
    acc = 2
    count = 2
    while (acc <= goal):
        acc = acc * 2
        count += 1

    arr = [1] * count
    arr[1] = n

    for i in range(2,count):
        arr[i] = (arr[i-1] * arr[i-1]) % m

    tbl = []
    tbl.append(0)
    for i in range(count-1):
        tbl.append(2**i)

    s2 = 0
    ac2 = 1
    for i in range(count-1, -1, -1):
        if s2 + tbl[i] > goal: continue
        else:
            s2 += tbl[i]
            ac2 *= arr[i]
            ac2 %= m

    print(ac2)

fastexp(0xc2, 0x11b, 254)
