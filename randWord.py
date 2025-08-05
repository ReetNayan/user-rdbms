import random


def genrt(length):
    s = ""
    for i in range(0, length):
        s = s+chr(random.randrange(97, 123))
    return s


def genrtNum(length, maxLimit):
    s = ""
    for i in range(0, length):
        s = s + str(random.randint(1, maxLimit))
    s = int(s)
    return s

def genrtIpAddr():
    ip=""
    for i in range(0,3):
        ip+=str(genrtNum(3, 5))+"."
    ip+=str(genrtNum(3, 5))
    return ip
print(genrtIpAddr())