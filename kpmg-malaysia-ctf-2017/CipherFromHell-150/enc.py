#!/usr/bin/env python2

m = open("message").read()
k = "key: 123".strip()
def gg(m, k):
    z = ""
    for i, c in enumerate(m):
        z += chr((ord(c)+ord(k[i%len(k)]))%256)

    print(z)
    return z
f = open("cipher", "wb")
f.write(gg(m, k))
f.close()


