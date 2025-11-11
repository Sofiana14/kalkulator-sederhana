import tkinter as tk
from tkinter import ttk, messagebox
from konstanta import *
from kalkulator_dasar import BasicCalculatorFrame 
from kalkulator_fungsi import FunctionCalculatorFrame 
from menu_konverter import ConverterUI
from split_bill_ui import SplitBillFrame # << UBAH: Import SplitBillFrame

# --- SETUP JENDELA UTAMA ---
root = tk.Tk()
root.title(APP_TITLE)
root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# Mengatur Style untuk ttk.Button agar serasi dengan tema gelap
# ... (Kode style tetap sama) ...
style = ttk.Style()
style.theme_use('alt')
style.configure('TButton',
                background=BTN_COLOR_NORMAL,
                foreground=TEXT_COLOR,
                bordercolor=BG_COLOR,
                borderwidth=0,
                focusthickness=3,
                focuscolor=FG_COLOR,
                padding=10)
style.map('TButton',
          background=[('active', BTN_COLOR_ACCENT)],
          foreground=[('active', FG_COLOR)])


# --- FRAME UTAMA UNTUK MENGGANTI TAMPILAN (Container) ---
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

# --- FUNGSI PEMBUKA UI EKSTERNAL ---
def open_converter_ui():
    ConverterUI(root)

# FIX: Fungsi open_split_bill_ui kini hanya memanggil show_frame
def open_split_bill_ui():
    """Mengalihkan tampilan ke SplitBillFrame di jendela yang sama."""
    show_frame("SplitBill")

def show_about_dialog():
    """Menampilkan dialog informasi aplikasi."""
    messagebox.showinfo(
        "Tentang Kalkulator Serbaguna", 
        f"{APP_TITLE}\nVersi 1.0\nDibuat menggunakan Python dan Tkinter.\n"
    )
    
# --- SETUP MENU BAR TKINTER ---
def setup_menu_bar():
    # 1. Buat Menu Bar utama
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar) 
    
    # 2. Menu "Mode" (Untuk Navigasi Cepat)
    mode_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Mode", menu=mode_menu)
    
    mode_menu.add_command(label="← Kembali ke Menu Utama", command=lambda: show_frame("Menu"))
    mode_menu.add_separator()
    mode_menu.add_command(label="Kalkulator Dasar", command=lambda: show_frame("KalkulatorDasar"))
    mode_menu.add_command(label="Kalkulator Fungsi", command=lambda: show_frame("KalkulatorFungsi"))
    mode_menu.add_separator()
    mode_menu.add_command(label="Converter", command=open_converter_ui)
    mode_menu.add_command(label="Split Bill", command=open_split_bill_ui)
    mode_menu.add_separator()
    mode_menu.add_command(label="Keluar Aplikasi", command=root.destroy)
    
    # 3. Menu "Bantuan"
    help_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Bantuan", menu=help_menu)
    
    help_menu.add_command(label="Tentang Aplikasi", command=show_about_dialog)

# --- Panggil SETUP MENU BAR ---
setup_menu_bar()

# --- 1. SETUP MENU UTAMA ---
menu_frame = tk.Frame(main_container, bg=BG_COLOR)
menu_frame.grid(row=0, column=0, sticky="nsew")
frames["Menu"] = menu_frame

title = tk.Label(menu_frame, text="Kalkulator Serbaguna", fg=FG_COLOR, bg=BG_COLOR, font=("Segoe UI", 18, "bold"))
title.pack(pady=30)

ttk.Button(menu_frame, text="Kalkulator Dasar", command=lambda: show_frame("KalkulatorDasar"), width=25).pack(pady=15)
ttk.Button(menu_frame, text="Kalkulator Fungsi", command=lambda: show_frame("KalkulatorFungsi"), width=25).pack(pady=15)
ttk.Button(menu_frame, text="Converter", command=open_converter_ui, width=25).pack(pady=15)
ttk.Button(menu_frame, text="Split Bill", command=open_split_bill_ui, width=25).pack(pady=15) # FIX: Memanggil open_split_bill_ui baru
ttk.Button(menu_frame, text="Keluar", command=root.destroy, width=25).pack(pady=40)


# --- 2. SETUP KALKULATOR DASAR ---
basic_calc_frame = BasicCalculatorFrame(main_container, lambda: show_frame("Menu"))
basic_calc_frame.grid(row=0, column=0, sticky="nsew")
frames["KalkulatorDasar"] = basic_calc_frame

# --- 3. SETUP KALKULATOR FUNGSI ---
function_calc_frame = FunctionCalculatorFrame(main_container, lambda: show_frame("Menu"))
function_calc_frame.grid(row=0, column=0, sticky="nsew")
frames["KalkulatorFungsi"] = function_calc_frame

# --- 4. SETUP SPLIT BILL (BARU) ---
split_bill_frame = SplitBillFrame(main_container, lambda: show_frame("Menu"))
split_bill_frame.grid(row=0, column=0, sticky="nsew")
frames["SplitBill"] = split_bill_frame # FIX: Tambahkan ke frames

# Tampilkan frame awal (Menu)
show_frame("Menu")

root.mainloop()