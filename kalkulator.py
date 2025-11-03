import tkinter as tk
from tkinter import messagebox  # tambahkan ini!

# ================== TEMA ==================
BG_UTAMA = "#000000"
BTN_DARK = "#2C2C2E"
BTN_OP = "#FF9500"
BTN_FUNC = "#444444"
BTN_MODE = "#FFD60A"
TEXT_WARNA = "white"

# ================== Aplikasi ==================
root = tk.Tk()
root.title("Kalkulator - Pilih Mode")
root.configure(bg=BG_UTAMA)
root.geometry("420x640")
root.resizable(False, False)

# ---------- State ----------
ekspresi = ""  # ekspresi yang sedang diketik pada kalkulator Basic

# ---------- Frame: Menu Utama (Pilihan 4 Mode) ----------
menu_frame = tk.Frame(root, bg=BG_UTAMA)
menu_frame.place(relwidth=1, relheight=1)

label_judul = tk.Label(menu_frame, text="Pilih Mode", font=("Arial", 28, "bold"),
                       bg=BG_UTAMA, fg=TEXT_WARNA)
label_judul.pack(pady=(40, 20))

desc = tk.Label(menu_frame, text="(UAS) Pilih salah satu mode di bawah", font=("Arial", 12),
                bg=BG_UTAMA, fg="#BBBBBB")
desc.pack(pady=(0, 20))

# ---------- Fungsi navigasi ----------
def buka_basic():
    menu_frame.place_forget()
    basic_frame.place(relwidth=1, relheight=1)

def buka_function():
    messagebox.showinfo("Info", "Mode Function belum diimplementasi di langkah ini.")

def buka_multi():
    messagebox.showinfo("Info", "Mode Multi belum diimplementasi di langkah ini.")

def buka_bmi():
    messagebox.showinfo("Info", "Mode BMI belum diimplementasi di langkah ini.")

# ---------- Tombol-tombol Mode ----------
left_col = tk.Frame(menu_frame, bg=BG_UTAMA)
left_col.pack(pady=10)

btn_basic = tk.Button(left_col, text="Kalkulator Basic", font=("Arial", 16, "bold"),
                      bg=BTN_MODE, fg="black", bd=0, padx=12, pady=12, command=buka_basic)
btn_function = tk.Button(left_col, text="Function", font=("Arial", 16, "bold"),
                         bg=BTN_FUNC, fg=TEXT_WARNA, bd=0, padx=12, pady=12, command=buka_function)
btn_multi = tk.Button(left_col, text="Multi", font=("Arial", 16, "bold"),
                      bg=BTN_FUNC, fg=TEXT_WARNA, bd=0, padx=12, pady=12, command=buka_multi)
btn_bmi = tk.Button(left_col, text="BMI", font=("Arial", 16, "bold"),
                    bg=BTN_FUNC, fg=TEXT_WARNA, bd=0, padx=12, pady=12, command=buka_bmi)

btn_basic.pack(fill="x", pady=8, ipadx=20)
btn_function.pack(fill="x", pady=8, ipadx=20)
btn_multi.pack(fill="x", pady=8, ipadx=20)
btn_bmi.pack(fill="x", pady=8, ipadx=20)

# ---------- Frame: Kalkulator Basic ----------
basic_frame = tk.Frame(root, bg=BG_UTAMA)
display_var = tk.StringVar(value="0")

display = tk.Label(basic_frame, textvariable=display_var, anchor="e",
                   font=("Consolas", 36, "bold"), bg=BG_UTAMA, fg=TEXT_WARNA,
                   padx=16, pady=16)
display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=(18, 8))

# ---------- Fungsi-fungsi kalkulator ----------
def update_display(val=None):
    if val is None:
        display_var.set(ekspresi if ekspresi else "0")
    else:
        display_var.set(val)

def tekan_tombol_basic(sym):
    global ekspresi
    ekspresi += str(sym)
    update_display()

def hapus_satu_basic():
    global ekspresi
    ekspresi = ekspresi[:-1]
    update_display()

def hapus_semua_basic():
    global ekspresi
    ekspresi = ""
    update_display("0")

def toggle_plus_minus():
    global ekspresi
    if not ekspresi:
        return
    import re
    m = re.search(r'(-?\d+(\.\d+)?|\.\d+)$', ekspresi)
    if not m:
        try:
            val = float(ekspresi)
            ekspresi = str(-val)
            update_display()
            return
        except:
            return
    num = m.group(0)
    start = m.start(0)
    if num.startswith("-"):
        newnum = num[1:]
    else:
        newnum = "-" + num
    ekspresi = ekspresi[:start] + newnum
    update_display()

def ubah_persen():
    global ekspresi
    import re
    m = re.search(r'(-?\d+(\.\d+)?|\.\d+)$', ekspresi)
    if not m:
        return
    num = m.group(0)
    start = m.start(0)
    try:
        val = float(num) / 100.0
        newstr = str(val).rstrip('0').rstrip('.') if '.' in str(val) else str(val)
        ekspresi = ekspresi[:start] + newstr
        update_display()
    except:
        update_display("Error")

def hitung_basic():
    global ekspresi
    if not ekspresi:
        update_display("0")
        return
    eksp = ekspresi.replace("×", "*").replace("÷", "/").replace("^", "**")
    try:
        hasil = eval(eksp, {}, {})
        if isinstance(hasil, float):
            hasil_str = str(round(hasil, 10)).rstrip('0').rstrip('.')
        else:
            hasil_str = str(hasil)
        update_display(hasil_str)
        ekspresi = hasil_str
    except Exception:
        update_display("Error")
        ekspresi = ""

# ---------- Layout tombol kalkulator ----------
tombol_layout = [
    ["AC", "Del", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["+/-", "0", ".", "^"],
]

def tombol_command(label):
    if label == "AC":
        hapus_semua_basic()
    elif label == "Del":
        hapus_satu_basic()
    elif label == "+/-":
        toggle_plus_minus()
    elif label == "%":
        ubah_persen()
    elif label == "=":
        hitung_basic()
    else:
        tekan_tombol_basic(label)

for r, baris in enumerate(tombol_layout, start=1):
    for c, label in enumerate(baris):
        bg = BTN_DARK
        fg = TEXT_WARNA
        if label in ["÷", "×", "-", "+", "^"]:
            bg = BTN_OP
        elif label in ["AC", "Del", "%", "+/-"]:
            bg = BTN_FUNC
        btn = tk.Button(basic_frame, text=label, font=("Arial", 20),
                        bg=bg, fg=fg, bd=0, command=lambda L=label: tombol_command(L))
        btn.grid(row=r, column=c, sticky="nsew", padx=6, pady=6)

# Tombol "="
btn_eq = tk.Button(basic_frame, text="=", font=("Arial", 20),
                   bg=BTN_OP, fg=TEXT_WARNA, bd=0, command=hitung_basic)
btn_eq.grid(row=6, column=3, sticky="nsew", padx=6, pady=6)

# Tombol "Kembali"
def kembali_ke_menu():
    global ekspresi
    ekspresi = ""
    basic_frame.place_forget()
    menu_frame.place(relwidth=1, relheight=1)

btn_back = tk.Button(basic_frame, text="Kembali", font=("Arial", 14),
                     bg=BTN_MODE, fg="black", command=kembali_ke_menu)
btn_back.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=6, pady=6)

# Grid proporsional
for i in range(7):
    basic_frame.grid_rowconfigure(i, weight=1)
for j in range(4):
    basic_frame.grid_columnconfigure(j, weight=1)

# ---------- Jalankan ----------
menu_frame.place(relwidth=1, relheight=1)
root.mainloop()
