def f2c(f_temp):
    c_temp = (f_temp - 32) * 5 / 9
    return c_temp

f_temp = int(input("몇도인가요?"))
print(f"화씨 {f_temp}도는 섭씨 {f2c(f_temp):.2f}도입니다.")