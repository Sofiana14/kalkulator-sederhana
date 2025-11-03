# function_mode.py
import tkinter as tk
import math

# Warna & gaya (senada dengan basic_mode)
BG = "#1c1c1c"
BTN_BG = "#333333"
BTN_ORANGE = "#FF9500"
BTN_BACK = "#FFD60A"
TEXT = "white"
FONT = ("Arial", 16, "bold")

def start_function(root, on_back):
    """
    Tampilkan kalkulator ilmiah rapi (layout serupa basic).
    on_back: callback untuk kembali ke menu utama.
    """
    # kosongkan root
    for w in root.winfo_children():
        w.destroy()

    root.title("Kalkulator Ilmiah")
    root.configure(bg=BG)

    # StringVar untuk layar
    expr_var = tk.StringVar(value="0")

    # helper untuk update layar
    def set_expr(s):
        expr_var.set(s)

    def append(s):
        cur = expr_var.get()
        if cur in ("0", "Error"):
            expr_var.set(s)
        else:
            expr_var.set(cur + s)

    # fungsi operasi khusus
    def clear():
        expr_var.set("0")

    def delete():
        cur = expr_var.get()
        if len(cur) <= 1:
            expr_var.set("0")
        else:
            expr_var.set(cur[:-1])

    def toggle_sign():
        cur = expr_var.get()
        try:
            # hanya jika cur adalah angka (simple)
            val = float(cur)
            expr_var.set(str(-val))
        except:
            pass

    def percent():
        cur = expr_var.get()
        try:
            val = float(eval(safe_expr(cur)))
            expr_var.set(str(val / 100.0))
        except:
            expr_var.set("Error")

    # factorial as immediate operation on current value
    def factorial_op():
        cur = expr_var.get()
        try:
            val = int(eval(safe_expr(cur)))
            expr_var.set(str(math.factorial(val)))
        except:
            expr_var.set("Error")

    # kalkulasi saat "=" ditekan
    def calculate():
        cur = expr_var.get()
        try:
            result = eval(safe_expr(cur), {"math": math})
            # format hasil ringkas
            if isinstance(result, float):
                s = str(round(result, 10)).rstrip("0").rstrip(".")
            else:
                s = str(result)
            expr_var.set(s)
        except:
            expr_var.set("Error")

    # ubah text expression ke bentuk yang bisa dieval (ganti fungsi → math.*)
    def safe_expr(s):
        # minimal replacements
        rep = {
            "×": "*",
            "÷": "/",
            "^": "**",
            "π": "math.pi",
            "√(": "math.sqrt(",
            "ln(": "math.log(",
            "log(": "math.log10(",
            "eˣ(": "math.exp(",
            "e": "math.e",  # note: if user uses scientific notation like 1e3 this may interfere;
                              # we insert math.e via button so typical expressions are fine.
        }
        # replace function names first to avoid partial conflicts
        s = s.replace("sin(", "math.sin(").replace("cos(", "math.cos(").replace("tan(", "math.tan(")
        s = s.replace("asin(", "math.asin(").replace("acos(", "math.acos(").replace("atan(", "math.atan(")
        s = s.replace("log(", "math.log10(").replace("ln(", "math.log(")
        # then replace tokens
        for k, v in rep.items():
            s = s.replace(k, v)
        return s

    # === LAYAR ===
    layar = tk.Label(root, textvariable=expr_var, bg=BG, fg=TEXT,
                     font=("Consolas", 30, "bold"), anchor="e", padx=20, pady=18)
    layar.grid(row=0, column=0, columnspan=5, sticky="nsew")

    # === pembuat tombol seragam ===
    def make_btn(text, row, col, cmd=None, bg=BTN_BG, colspan=1):
        b = tk.Button(root, text=text, command=cmd or (lambda t=text: append(t)),
                      bg=bg, fg=TEXT, font=FONT, relief="flat", bd=0)
        b.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=1, pady=1)
        return b

    # === SUSUNAN TOMBOL (rapi, operator oranye di kanan, tombol Kembali kuning) ===
    # baris 1
    make_btn("AC", 1, 0, cmd=clear, bg=BTN_BG)
    make_btn("Del", 1, 1, cmd=delete, bg=BTN_BG)
    make_btn("%", 1, 2, cmd=percent, bg=BTN_BG)
    make_btn("^", 1, 3, cmd=lambda: append("^"), bg=BTN_BG)
    make_btn("÷", 1, 4, cmd=lambda: append("÷"), bg=BTN_ORANGE)

    # baris 2 (fungsi ilmiah)
    make_btn("sin", 2, 0, cmd=lambda: append("sin("))
    make_btn("cos", 2, 1, cmd=lambda: append("cos("))
    make_btn("tan", 2, 2, cmd=lambda: append("tan("))
    make_btn("log", 2, 3, cmd=lambda: append("log("))
    make_btn("×", 2, 4, cmd=lambda: append("×"), bg=BTN_ORANGE)

    # baris 3
    make_btn("asin", 3, 0, cmd=lambda: append("asin("))
    make_btn("acos", 3, 1, cmd=lambda: append("acos("))
    make_btn("atan", 3, 2, cmd=lambda: append("atan("))
    make_btn("ln", 3, 3, cmd=lambda: append("ln("))
    make_btn("-", 3, 4, cmd=lambda: append("-"), bg=BTN_ORANGE)

    # baris 4
    make_btn("√", 4, 0, cmd=lambda: append("√("))
    make_btn("x²", 4, 1, cmd=lambda: append("**2"))
    make_btn("x³", 4, 2, cmd=lambda: append("**3"))
    make_btn("xʸ", 4, 3, cmd=lambda: append("^"))
    make_btn("+", 4, 4, cmd=lambda: append("+"), bg=BTN_ORANGE)

    # baris 5 (digits)
    make_btn("7", 5, 0); make_btn("8", 5, 1); make_btn("9", 5, 2)
    make_btn("(", 5, 3, cmd=lambda: append("("))
    make_btn(")", 5, 4, cmd=lambda: append(")"), bg=BTN_ORANGE)

    # baris 6
    make_btn("4", 6, 0); make_btn("5", 6, 1); make_btn("6", 6, 2)
    make_btn("1/x", 6, 3, cmd=lambda: append("1/("))
    make_btn("|x|", 6, 4, cmd=lambda: append("abs("), bg=BTN_ORANGE)

    # baris 7
    make_btn("1", 7, 0); make_btn("2", 7, 1); make_btn("3", 7, 2)
    make_btn("π", 7, 3, cmd=lambda: append("π"))
    make_btn("e", 7, 4, cmd=lambda: append("e"), bg=BTN_ORANGE)

    # baris 8 (bawah)
    make_btn("+/-", 8, 0, cmd=toggle_sign)
    make_btn("0", 8, 1)
    make_btn(".", 8, 2)
    make_btn("!", 8, 3, cmd=factorial_op)
    make_btn("=", 8, 4, cmd=calculate, bg=BTN_ORANGE)

    # baris 9: tombol Kembali menutup "celah" bawah kiri
    make_btn("Kembali", 9, 0, cmd=on_back, bg=BTN_BACK, colspan=3)
    # isi kanan bawah kosong agar simetris (gunakan frame kosong berwarna BG)
    filler = tk.Frame(root, bg=BTN_BG)
    filler.grid(row=9, column=3, columnspan=2, sticky="nsew", padx=1, pady=1)

    # grid scaling agar tombol memenuhi area tanpa celah besar
    rows = 10
    cols = 5
    for r in range(rows):
        root.grid_rowconfigure(r, weight=1)
    for c in range(cols):
        root.grid_columnconfigure(c, weight=1)
