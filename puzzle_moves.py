MIN_VAL = 1
MAX_VAL = 1000000


def add_sub_n(start, n): 
    if start + n > MAX_VAL or start + n < MIN_VAL:
        return start
    return start + n


def mult_div_n(start, n):
    n //= 10
    if n > 0:
        if start*n > MAX_VAL:
            return start
        return start*n
    n *= -1
    if start % n != 0:
        return start
    return start // n


def raise_root_n(start, n):
    n //= 1000
    if n > 0:
        if start ** n > MAX_VAL:
            return start
        return start ** n
    n *= -1
    if round(start**(1/n))**n != start:
        return start
    return int(round(start**(1/n)))


def get_operation(n):
    if n % 1000 == 0:
        return raise_root_n
    elif n % 10 == 0:
        return mult_div_n
    else:
        return add_sub_n
