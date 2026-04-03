def is_prime(num):
    if num <= 1:
        return False

    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


def get_primes_below(n):
    primes = []
    for i in range(2, n + 1):
        if is_prime(i):
            primes.append(i)
    return primes


limit = int(input("숫자를 입력하세요: "))
result = get_primes_below(limit)

print(f"\n{limit} 이하의 소수 목록:")
print(result)
