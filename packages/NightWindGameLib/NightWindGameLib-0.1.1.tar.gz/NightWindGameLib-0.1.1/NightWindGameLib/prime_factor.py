import math

# 分解质因数
def prime(n: int):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def get_prime_factor(num):
    number = num
    List = []
    if num >= 2:
        while number > 1:
            for i in range(2, number + 1):
                if prime(i):
                    if number % i == 0:     
                        List.append(str(i))
                        number = number//i
                        break
    return List
