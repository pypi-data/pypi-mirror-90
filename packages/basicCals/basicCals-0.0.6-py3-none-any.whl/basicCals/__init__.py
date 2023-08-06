def add(addend1, addend2):
    if(isinstance(addend1, str) == True):
        print("Value can't be a string!")
    if(isinstance(addend1, str) == False and isinstance(addend2, str) == False):
        if(addend1 - int(addend1) == 0 and addend2 - int(addend2) == 0):
            return int(addend1) + int(addend2)
        if(addend1 - int(addend1) != 0 or addend1 - int(addend1) != 0):
            return float(addend1) + float(addend2)

def subtract(minuend, subtrahend):
    if(isinstance(minuend, str) == True or isinstance(subtrahend, str) == True):
        print("Value cannot be a string")
    if(isinstance(minuend, str) == False and isinstance(subtrahend, str) == False):
        if(minuend - int(minuend) == 0 and subtrahend - int(subtrahend) == 0):
            return int(minuend) - int(subtrahend)
        if(minuend - int(minuend) != 0 or subtrahend - int(subtrahend) != 0):
            return float(minuend) - float(subtrahend)


def multiply(multiplier, multiplicand):
    if(isinstance(multiplier, str) == True or isinstance(multiplicand, str) == True):
        print("Value cannot be a string")
    if(isinstance(multiplier, str) == False and isinstance(multiplicand, str) == False):
        if(multiplier - int(multiplier) == 0 and multiplicand - int(multiplicand) == 0):
            return int(multiplier) * int(multiplicand)
        if(multiplier - int(multiplier) != 0 or multiplicand - int(multiplicand) != 0):
            return float(multiplier) * float(multiplicand)
    
def divide(dividend, divisor):
    if(isinstance(dividend, str) == True or isinstance(divisor, str) == True):
        print("Value cannot be a string")
    if(isinstance(dividend, str) == False and isinstance(divisor, str) == False):
        if(dividend - int(dividend) == 0 and divisor - int(divisor) == 0):
            return int(dividend) / int(divisor)
        if(dividend - int(dividend) != 0 or divisor - int(divisor) != 0):
            return float(dividend) / float(divisor)


def power(base, exponent):
    if(isinstance(base, str) == True or isinstance(exponent, str) == True):
        print("Value cannot be a string")
    if(isinstance(base, str) == False and isinstance(exponent, str) == False):
        if(base - int(base) == 0 and exponent - int(exponent) == 0):
            return int(base) ** int(exponent)
        if(base - int(base) != 0 or exponent - int(exponent) != 0):
            return float(base) ** float(exponent)


def mean(inList):
    return sum(inList) / len(inList)


def sub(minuend, subtrahend):
    if(isinstance(minuend, str) == True or isinstance(subtrahend, str) == True):
        print("Value cannot be a string")
    if(isinstance(minuend, str) == False and isinstance(subtrahend, str) == False):
        if(minuend - int(minuend) == 0 and subtrahend - int(subtrahend) == 0):
            return int(minuend) - int(subtrahend)
        if(minuend - int(minuend) != 0 or subtrahend - int(subtrahend) != 0):
            return float(minuend) - float(subtrahend)

def mul(multiplier, multiplicand):
    if(isinstance(multiplier, str) == True or isinstance(multiplicand, str) == True):
        print("Value cannot be a string")
    if(isinstance(multiplier, str) == False and isinstance(multiplicand, str) == False):
        if(multiplier - int(multiplier) == 0 and multiplicand - int(multiplicand) == 0):
            return int(multiplier) * int(multiplicand)
        if(multiplier - int(multiplier) != 0 or multiplicand - int(multiplicand) != 0):
            return float(multiplier) * float(multiplicand)
 
def div(dividend, divisor):
    if(isinstance(dividend, str) == True or isinstance(divisor, str) == True):
        print("Value cannot be a string")
    if(isinstance(dividend, str) == False and isinstance(divisor, str) == False):
        if(dividend - int(dividend) == 0 and divisor - int(divisor) == 0):
            return int(dividend) / int(divisor)
        if(dividend - int(dividend) != 0 or divisor - int(divisor) != 0):
            return float(dividend) / float(divisor)

def pow(base, exponent):
    if(isinstance(base, str) == True or isinstance(exponent, str) == True):
        print("Value cannot be a string")
    if(isinstance(base, str) == False and isinstance(exponent, str) == False):
        if(base - int(base) == 0 and exponent - int(exponent) == 0):
            return int(base) ** int(exponent)
        if(base - int(base) != 0 or exponent - int(exponent) != 0):
            return float(base) ** float(exponent)