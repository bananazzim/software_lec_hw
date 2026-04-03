def factorial(n):
    
    if n <= 1:
        return 1
    
    return n * factorial(n - 1)

num = int(input("팩토리얼을 구할 숫자를 입력하세요: "))

if num < 0:
    print("음수의 팩토리얼은 정의되지 않습니다.")
else:
    result = factorial(num)
    print(f"{num}! 의 결과는 {result}입니다.")