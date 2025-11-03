import tkinter as tk

BG_UTAMA = "#000000"
BTN_DARK = "#2C2C2E"
BTN_OP = "#FF9500"
BTN_FUNC = "#444444"
BTN_MODE = "#FFD60A"
TEXT_WARNA = "white"

def start_basic(root, on_back):
    """
    Tampilkan UI Kalkulator Basic pada `root`.
    on_back: callback yang dipanggil ketika pengguna menekan tombol Kembali.
    """
    # Hapus semua widget di root
    for w in root.winfo_children():
        w.destroy()

    frame = tk.Frame(root, bg=BG_UTAMA)
    frame.place(relwidth=1, relheight=1)

    display_var = tk.StringVar(value="0")
    layar = tk.Label(frame, textvariable=display_var, font=("Consolas", 36, "bold"),
                     bg=BG_UTAMA, fg=TEXT_WARNA, anchor="e", padx=16, pady=16)
    layar.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=(18, 8))

    ekspresi = ""  # lokal untuk start_basic

    def update_display(val=None):
        if val is None:
            display_var.set(ekspresi if ekspresi else "0")
        else:
            display_var.set(val)

    # gunakan nonlocal agar nested function dapat memodifikasi ekspresi lokal
    def tekan(simbol):
        nonlocal ekspresi
        ekspresi += str(simbol)
        update_display()

    def hapus():
        nonlocal ekspresi
        ekspresi = ekspresi[:-1]
        update_display()

    def clear():
        nonlocal ekspresi
        ekspresi = ""
        update_display("0")

    def hitung():
        nonlocal ekspresi
        if not ekspresi:
            update_display("0")
            return
        eksp = ekspresi.replace("×", "*").replace("÷", "/").replace("^", "**")
        try:
            # safety: kita hanya menilai arithmetic sederhana
            hasil = eval(eksp, {}, {})
            if isinstance(hasil, float):
                hasil_str = str(round(hasil, 10)).rstrip("0").rstrip(".")
            else:
                hasil_str = str(hasil)
            ekspresi = hasil_str
            update_display(hasil_str)
        except Exception:
            ekspresi = ""
            update_display("Error")

    def toggle_plus_minus():
        nonlocal ekspresi
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
        nonlocal ekspresi
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

    # Layout tombol
    tombol_layout = [
        ["AC", "Del", "%", "÷"],
        ["7", "8", "9", "×"],
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        ["+/-", "0", ".", "^"],
    ]

    def tombol_action(label):
        if label == "AC":
            clear()
        elif label == "Del":
            hapus()
        elif label == "+/-":
            toggle_plus_minus()
        elif label == "%":
            ubah_persen()
        elif label == "=":
            hitung()
        else:
            tekan(label)

    for r, baris in enumerate(tombol_layout, start=1):
        for c, label in enumerate(baris):
            bg = BTN_DARK
            fg = TEXT_WARNA
            if label in ["÷", "×", "-", "+", "^"]:
                bg = BTN_OP
            elif label in ["AC", "Del", "%", "+/-"]:
                bg = BTN_FUNC
            btn = tk.Button(frame, text=label, font=("Arial", 20), bg=bg, fg=fg, bd=0,
                            command=lambda L=label: tombol_action(L))
            btn.grid(row=r, column=c, sticky="nsew", padx=6, pady=6)

    # Tombol "=" (terpisah agar tampilan rapi)
    btn_eq = tk.Button(frame, text="=", font=("Arial", 20), bg=BTN_OP, fg=TEXT_WARNA, bd=0, command=hitung)
    btn_eq.grid(row=6, column=3, sticky="nsew", padx=6, pady=6)

    # Tombol kembali: panggil callback on_back()
    btn_back = tk.Button(frame, text="Kembali", font=("Arial", 14), bg=BTN_MODE, fg="black",
                         command=lambda: on_back())
    btn_back.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=6, pady=6)

    # grid proporsional
    for i in range(8):
        frame.grid_rowconfigure(i, weight=1)
    for j in range(4):
        frame.grid_columnconfigure(j, weight=1)
