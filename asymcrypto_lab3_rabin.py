import random
import math
from algnuth.jacobi import jacobi
import random
from random import randrange
def find_s(n):
    count = 0
    temp = n - 1
    flag = 0
    if n%2 == 0:
        return False,0
    else:
        while flag == 0:
            temp /= 2
            count+=1
            if temp%2 == 1:
                break
    return count,int((n-1)/(2**count))

def miller_rabin_test(n: int):
    x = 0
    k = 10
    s,t = find_s(n)
    if not(s):
        return True
    for i in range(k):
        a = random.randrange(2, n)
        x = pow(a, t, n)
        if x == 1 or x == n-1:
            continue
        for i in range(s-1):
            x = (x**2) % n
            if x == 1:
                return False
            if x == n-1:
                break
        if x==n-1:
            continue
        return False
    return True

def gen_pr():
    n_0 = 1
    n_1 = 2**64
    x = random.randrange(n_0, n_1)
    if x%2 == 0:
        x+=1
    for i in range(0,n_1-n_0):
        x+=2*i
        if miller_rabin_test(x):
            break
    return x

def format_mes(M, l):
    r = gen_pr()
    return 255*2**(8*(l-2)) + M*2**64 + r

def unformat_mes(x, l):
    r = x&0xFFFF_FFFF_FFFF_FFFF
    return (x - 255*2**(8*(l-2)) - r) // (2**64)

def gen_keys():
    p = gen_pr(2**128, 2**256)
    print("Ok")
    q = gen_pr(2**256, 2**512)
    b = gen_pr(2**256, 2**512)
    n = p*q
    return [(p, q, b), (n, b)]

def evkl(p, q):
    if(p == 0):
        return q, 0, 1

    else:
        temp_1 = q//p
        temp_2 = q%p
        
        d, x_1, y_1 = evkl(temp_2, p)
        x = y_1 - (q//p) * x_1
        y = x_1
        return d, x, y
    
def sqrt_mod(y,p,q):
    n = p*q
    s_1 = pow(y,(p+1)//4,p)
    s_2 = pow(y,(q+1)//4,q)
    d, u, v  = evkl(p, q)
    return (u*p*s_2 + v*q*s_1)%n, (-u*p*s_2 + v*q*s_1)%n, (u*p*s_2 - v*q*s_1)%n, (-u*p*s_2 - v*q*s_1)%n


def encrypt(M, n, b):
    l = (len(bin(n))-2)//8
    x = format_mes(M,l)
    y = (x*(x + b)) % n
    c1 = (x + b * pow(2,-1,n))%n%2
    c2 = int(jacobi((x + b * pow(2,-1,n)),n)==1)
    return y, c1, c2

def decrypt(y,c_1,c_2,p,q,b):
    n = p*q
    l = (len(bin(n))-2)//8
    sqrts = sqrt_mod((y+((b**2)%n)*pow(4,-1,n))%n, p,q)
    x = []
    for i in sqrts:
        x_1 = (-b*pow(2,-1,n)+i)%n
        c_1_t = (x_1 + b * pow(2,-1,n))%n%2
        c_2_t = int(jacobi((x_1 + b * pow(2,-1,n)),n)==1)
        if c_1_t == c_1 and c_2_t == c_2:
            M = unformat_mes(x_1, l)
            return M

def signification(M, p, q):
    n = p*q
    l = (len(bin(n))-2)//8
    x = format_mes(M, l)
    c1, c2= jacobi(x, p), jacobi(x, q)
    while c1 != 1 or c2!=1:
        x = format_mes(M,l)
        c1, c2= jacobi(x, p), jacobi(x, q)
        print("Ok")
    sq = sqrt_mod(x,p,q)
    
    s = sq[0]
    print("M = ", hex(M)[2:])
    print("s = ", hex(s)[2:])
    print("n = ", hex(n)[2:])
    return M, s

def ver(M, s, n):
    l = (len(bin(n))-2)//8
    x_temp = pow(s, 2, n)
    return unformat_mes(x_temp, l) == M

def atack(n):
    t = randrange(1, n)
    y = pow(t, 2, n)
    print(hex(y)[2:])
    z = int(input("z = "), 16)
    while z == t or z == -t%n:
        t = randrange(1, n)
        y = pow(t, 2, n)
        z = int(input("z = "), 16)
    p = evkl(t+z, n)[0]
    q = n//p
    print("q = ", hex(q))
    print("p = ", hex(p))

def main(M,p,q,b):
    print("p = ", hex(p)[2:])
    print("q = ", hex(q)[2:])
    print("n = ", hex(p*q)[2:])
    print("b = ", hex(b)[2:])
    print("M = ", hex(M)[2:])
    
    y = int("0x"+input("Ciphertext = "),16)
    print(y)
    c1 = int(input("Parity = "))
    c2 = int(input("Jacobi Symbol = "))
    print(hex(decrypt(y,c1,c2,p,q,b)))

    n_temp = int("0x"+input("Modulus = "),16)
    b = int("0x"+input("B = "),16)
    result = encrypt(M,n_temp,b)
    print("Ciphertext = ", hex(result[0])[2:])
    print("Parity = ", hex(result[1])[2:])
    print("Jacobi Symbol = ", hex(result[2])[2:])
    
    n_temp = int("0x"+input("Modulus = "),16)
    s = int("0x"+input("Signature = "),16)
    print(ver(M,s,n_temp))

    res = signification(M,p,q)[1]
    print("Atack")
    n_temp_2 = int("0x"+input("Modulus = "),16)
    atack(n_temp_2)
    
    
p = int(0xe5ebc2a6f9bc04da6538a1361922301f)
q = int(0xc6320fa9d7e1803e0a2028f21a12d113)
b = int(0x91DD5D1C6A913A1DE7A77285F40A0804D18D2929111E4D625EA374D9FE50B44B)
M = 12345678
main(M,p,q,b)
