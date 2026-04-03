import tkinter as tk
from tkinter import scrolledtext

def is_prime(num):
    if num <= 1: return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0: return False
    return True

def get_primes():
    try:
        limit = int(entry.get())
        primes = [str(i) for i in range(2, limit + 1) if is_prime(i)]
        
        # 소수 판별 결과
        status = "소수입니다" if is_prime(limit) else "소수가 아닙니다"
        label_status.config(text=f"입력값 {limit}: {status}")
        
        # 목록 출력
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.INSERT, ", ".join(primes))
    except ValueError:
        label_status.config(text="정수를 입력하세요", fg="red")

root = tk.Tk()
root.title("소수 마스터")
root.geometry("400x400")

tk.Label(root, text="숫자 입력 (해당 숫자 이하 소수 찾기)", font=("Pretendard", 10)).pack(pady=10)
entry = tk.Entry(root, font=("Pretendard", 12))
entry.pack()

tk.Button(root, text="소수 분석", command=get_primes, bg="#00796B", fg="white").pack(pady=10)
label_status = tk.Label(root, text="결과 대기 중...", font=("Pretendard", 11, "bold"))
label_status.pack()

tk.Label(root, text="소수 목록:").pack(pady=5)
text_area = scrolledtext.ScrolledText(root, width=40, height=10, font=("Consolas", 10))
text_area.pack(pady=5)

root.mainloop()