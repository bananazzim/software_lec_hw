import tkinter as tk
from tkinter import messagebox

def factorial(n):
    if n <= 1: return 1
    return n * factorial(n - 1)

def calculate():
    try:
        num = int(entry.get())
        if num < 0:
            label_result.config(text="음수는 계산할 수 없습니다.", fg="red")
        elif num > 100: # 재귀 깊이 제한 고려
            label_result.config(text="너무 큰 숫자는 계산이 어렵습니다.", fg="red")
        else:
            result = factorial(num)
            label_result.config(text=f"결과: {result}", fg="#4527A0")
    except ValueError:
        messagebox.showerror("입력 오류", "정수를 입력해주세요.")

root = tk.Tk()
root.title("팩토리얼 계산기")
root.geometry("350x250")

tk.Label(root, text="팩토리얼을 구할 숫자 입력", font=("Pretendard", 11)).pack(pady=20)
entry = tk.Entry(root, font=("Pretendard", 12), justify='center')
entry.pack(pady=5)

tk.Button(root, text="계산 시작", command=calculate, bg="#673AB7", fg="white", font=("bold")).pack(pady=20)
label_result = tk.Label(root, text="결과값이 표시됩니다.", font=("Pretendard", 10))
label_result.pack()

root.mainloop()