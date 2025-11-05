# utama.py

import tkinter as tk
from tkinter import ttk
from konstanta import *
from kalkulator_dasar import open_basic_calculator
from kalkulator_fungsi import open_function_calculator
from menu_konverter import ConverterUI

root = tk.Tk()
root.title(APP_TITLE)
root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# Mengatur Style untuk ttk.Button agar serasi dengan tema gelap
style = ttk.Style()
style.theme_use('alt') 

# Style untuk tombol menu utama
style.configure('TButton', 
                background=BTN_COLOR_NORMAL, 
                foreground=TEXT_COLOR,
                bordercolor=BG_COLOR,
                borderwidth=0,
                focusthickness=3,
                focuscolor=FG_COLOR,
                padding=10)
# Style ketika tombol ditekan
style.map('TButton', 
          background=[('active', BTN_COLOR_ACCENT)],
          foreground=[('active', FG_COLOR)])


title = tk.Label(root, text="Kalkulator Serbaguna", fg=FG_COLOR, bg=BG_COLOR, font=("Segoe UI", 18, "bold"))
title.pack(pady=30)

# Panggil fungsi yang sudah diimpor dari file terpisah
ttk.Button(root, text="Kalkulator Dasar", command=lambda: open_basic_calculator(root), width=25).pack(pady=15)
ttk.Button(root, text="Kalkulator Fungsi", command=lambda: open_function_calculator(root), width=25).pack(pady=15)
ttk.Button(root, text="Converter", command=lambda: ConverterUI(root), width=25).pack(pady=15)

# Tombol keluar
ttk.Button(root, text="Keluar", command=root.destroy, width=25).pack(pady=40)

root.mainloop()