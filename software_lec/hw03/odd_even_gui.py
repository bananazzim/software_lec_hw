import tkinter as tk

def check():
    try:
        num = int(entry.get())
        res = "짝수" if num % 2 == 0 else "홀수"
        color = "#0288D1" if res == "짝수" else "#D32F2F"
        label_result.config(text=f"{num}은(는) {res}입니다.", fg=color)
    except ValueError:
        label_result.config(text="숫자만 입력 가능합니다.", fg="red")

root = tk.Tk()
root.title("홀짝 판별기")
root.geometry("300x200")

tk.Label(root, text="정수 입력", font=("Pretendard", 12)).pack(pady=10)
entry = tk.Entry(root, font=("Pretendard", 12))
entry.pack()

tk.Button(root, text="확인", command=check, width=10, bg="#424242", fg="white").pack(pady=20)
label_result = tk.Label(root, text="숫자를 입력하고 확인을 누르세요", font=("Pretendard", 10))
label_result.pack()

root.mainloop()