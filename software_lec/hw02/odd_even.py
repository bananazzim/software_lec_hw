def odd_even(num):
 if num % 2 == 0:
    print(f"{num}은(는) 짝수입니다.")
 else:
    print(f"{num}은(는) 홀수입니다.")

num = int(input("숫자를 입력하세요: "))

odd_even(num)