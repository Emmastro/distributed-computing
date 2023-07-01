"""returns the task Id"""
import json

RANGE_TO_CHECK = 1000000

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def get_prime_numbers(n):
    start = (n - 1) * RANGE_TO_CHECK
    end = n * RANGE_TO_CHECK
    prime_numbers = []
    for i in range(start, end):
        if is_prime(i):
            prime_numbers.append(i)
    return sum(prime_numbers)

def main(task_id):
    result = get_prime_numbers(task_id)

    return json.dumps(result)


if __name__ == "__main__":
    result = main(10000)
    print(result)