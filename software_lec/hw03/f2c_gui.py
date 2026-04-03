import tkinter as tk
from tkinter import messagebox

def convert():
    try:
        f_temp = float(entry.get())
        c_temp = (f_temp - 32) * 5 / 9
        label_result.config(text=f"결과: 섭씨 {c_temp:.2f} ℃", fg="#2E7D32")
    except ValueError:
        messagebox.showerror("입력 오류", "숫자를 입력해주세요.")

root = tk.Tk()
root.title("온도 변환기")
root.geometry("300x200")
root.configure(bg="#F5F5F5")

tk.Label(root, text="화씨 온도를 입력하세요", bg="#F5F5F5", font=("Pretendard", 10)).pack(pady=10)
entry = tk.Entry(root, font=("Pretendard", 12))
entry.pack(pady=5)

btn = tk.Button(root, text="변환하기", command=convert, bg="#1976D2", fg="white", width=15)
btn.pack(pady=15)

label_result = tk.Label(root, text="결과가 여기에 표시됩니다", bg="#F5F5F5", font=("Pretendard", 11, "bold"))
label_result.pack()

root.mainloop()