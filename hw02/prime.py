def is_prime(n):

    if n <= 1:
        return False
    
  
    for i in range(2, n):
        if n % i == 0:
            return False
            

    return True


num = int(input("판별할 정수를 입력하세요: "))

if is_prime(num):
    print(f"결과: {num}은(는) 소수입니다.")
else:
    print(f"결과: {num}은(는) 소수가 아닙니다.")