import tkinter as tk

def run_sum():
    even_list = [i for i in range(1, 101) if i % 2 == 0]
    total = sum(even_list)
    label_res.config(text=f"합계: {total}", font=("Pretendard", 20, "bold"), fg="#E64A19")
    label_desc.config(text="1부터 100까지의 모든 짝수를 더한 결과입니다.")

root = tk.Tk()
root.title("짝수 합 계산기")
root.geometry("350x200")

tk.Label(root, text="1~100 짝수 합 구하기", font=("Pretendard", 12)).pack(pady=10)
tk.Button(root, text="계산 실행", command=run_sum, bg="#F4511E", fg="white", padx=20).pack(pady=10)

label_res = tk.Label(root, text="?", font=("Pretendard", 15))
label_res.pack()
label_desc = tk.Label(root, text="", font=("Pretendard", 9), fg="gray")
label_desc.pack()

root.mainloop()