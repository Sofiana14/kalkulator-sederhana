import tkinter as tk
from tkinter import ttk
from konstanta import *
from kalkulator_dasar import BasicCalculatorFrame # Import kelas Frame baru
from kalkulator_fungsi import FunctionCalculatorFrame # Import kelas Frame baru
from menu_konverter import ConverterUI

# --- SETUP JENDELA UTAMA ---
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


# --- FRAME UTAMA UNTUK MENGGANTI TAMPILAN (Container) ---
# Frame ini akan menjadi wadah untuk semua tampilan (Menu, Kalkulator Dasar, Kalkulator Fungsi)
main_container = tk.Frame(root, bg=BG_COLOR)
main_container.pack(fill="both", expand=True)
main_container.grid_rowconfigure(0, weight=1)
main_container.grid_columnconfigure(0, weight=1)

# Daftar frame yang tersedia
frames = {}

# --- FUNGSI PENGATUR TAMPILAN (SWITCHER) ---
def show_frame(frame_name):
    """Menampilkan frame yang diminta dan menyembunyikan yang lain."""
    frame = frames[frame_name]
    frame.tkraise()


# --- 1. SETUP MENU UTAMA ---
menu_frame = tk.Frame(main_container, bg=BG_COLOR)
menu_frame.grid(row=0, column=0, sticky="nsew")
frames["Menu"] = menu_frame

title = tk.Label(menu_frame, text="Kalkulator Serbaguna", fg=FG_COLOR, bg=BG_COLOR, font=("Segoe UI", 18, "bold"))
title.pack(pady=30)

# Tombol untuk beralih ke Kalkulator Dasar
ttk.Button(menu_frame, text="Kalkulator Dasar", command=lambda: show_frame("KalkulatorDasar"), width=25).pack(pady=15)
# Tombol untuk beralih ke Kalkulator Fungsi
ttk.Button(menu_frame, text="Kalkulator Fungsi", command=lambda: show_frame("KalkulatorFungsi"), width=25).pack(pady=15)
# Tombol Converter (Jika ConverterUI bisa diubah menjadi Frame, ini akan lebih baik. Saat ini tetap menggunakan TopLevel/Root)
ttk.Button(menu_frame, text="Converter", command=lambda: ConverterUI(root), width=25).pack(pady=15)

# Tombol keluar
ttk.Button(menu_frame, text="Keluar", command=root.destroy, width=25).pack(pady=40)


# --- 2. SETUP KALKULATOR DASAR ---
# BasicCalculatorFrame kini menginisialisasi dirinya di dalam main_container
# dan menerima fungsi `show_frame` sebagai callback untuk tombol "Kembali"
basic_calc_frame = BasicCalculatorFrame(main_container, lambda: show_frame("Menu"))
basic_calc_frame.grid(row=0, column=0, sticky="nsew")
frames["KalkulatorDasar"] = basic_calc_frame

# --- 3. SETUP KALKULATOR FUNGSI ---
function_calc_frame = FunctionCalculatorFrame(main_container, lambda: show_frame("Menu"))
function_calc_frame.grid(row=0, column=0, sticky="nsew")
frames["KalkulatorFungsi"] = function_calc_frame


# Tampilkan frame awal (Menu)
show_frame("Menu")

root.mainloop()