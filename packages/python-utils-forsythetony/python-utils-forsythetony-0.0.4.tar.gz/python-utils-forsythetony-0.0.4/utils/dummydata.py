import string
import random

INT_UPPER_BOUND = 10000

def random_list(type, count: int) -> list:
    
    if type == str:
        return random_string_list(count)
    elif type == int:
        return 


    raise NotImplementedError(f"The type ({type}) is not implemented")


def random_string(count: int = 10, chars = string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(count))

def random_string_list(count: int) -> list[str]:
    return [random_string() for _ in range(count)]

def random_int_list(count: int, upper_bound: int = INT_UPPER_BOUND) -> list[int]:
    return [random.randint(0, upper_bound) for _ in range(count)]
