import tkinter as tk
import math

# --- 1. PENGATURAN TEMA WARNA IOS DARK MODE ---
BG_UTAMA = "#000000"        # Hitam Penuh
BTN_DARK_GREY = "#333333"   # Tombol Angka (Abu-abu gelap)
BTN_LIGHT_GREY = "#666666"  # Tombol Fungsi (AC, +/-, %)
BTN_ORANGE = "#FF9500"      # Tombol Operator Utama
TEXT_WARNA = "white"

# --- 2. VARIABEL DAN FUNGSI UTAMA ---
ekspresi_sekarang = ""
hasil_display = None

def format_angka(angka_str):
    """Memformat angka dengan titik ribuan (pemisah desimal koma)."""
    try:
        clean_str = str(angka_str).replace('.', '').replace(',', '.') 
        
        is_negative = clean_str.startswith('-')
        if is_negative:
            clean_str = clean_str[1:]

        if '.' in clean_str:
            integer_part, decimal_part = clean_str.split('.')
        else:
            integer_part, decimal_part = clean_str, ''
        
        formatted_integer = "{:,}".format(int(integer_part)).replace(",", ".")

        result = formatted_integer
        if decimal_part:
            result += "," + decimal_part
            
        return "-" + result if is_negative else result
    except:
        return str(angka_str)


def update_tampilan():
    """Memperbarui layar tampilan."""
    # Selama ekspresi_sekarang tidak mengandung operator, format sebagai angka.
    if all(c not in ekspresi_sekarang for c in '+-*/'):
        hasil_display.set(format_angka(ekspresi_sekarang))
    else:
        # Jika ada operator, tampilkan ekspresi tanpa format ribuan
        hasil_display.set(ekspresi_sekarang)


def tekan_tombol(simbol):
    """Menambahkan simbol angka/operator."""
    global ekspresi_sekarang
    simbol_str = str(simbol)
    
    # Pencegahan double operator
    if simbol_str in '+-*/' and ekspresi_sekarang and ekspresi_sekarang[-1] in '+-*/':
        ekspresi_sekarang = ekspresi_sekarang[:-1] + simbol_str
    else:
        ekspresi_sekarang += simbol_str
    
    update_tampilan()


def hapus_semua():
    """Hapus semua ekspresi (AC)."""
    global ekspresi_sekarang
    ekspresi_sekarang = "0"
    hasil_display.set("0")
    ekspresi_sekarang = ""

def hapus_satu_karakter():
    """Hapus karakter terakhir."""
    global ekspresi_sekarang
    ekspresi_sekarang = ekspresi_sekarang[:-1]
    if not ekspresi_sekarang:
        hapus_semua()
    else:
        update_tampilan()


def hitung_hasil():
    """Menghitung ekspresi dan menampilkan hasil dengan format."""
    global ekspresi_sekarang
    try:
        # Gantikan sin(), cos(), dll. di ekspresi jika ada
        temp_exp = ekspresi_sekarang.replace('^', '**')

        hasil = eval(temp_exp)
        hasil_str = str(round(hasil, 10))

        hasil_display.set(format_angka(hasil_str))
        ekspresi_sekarang = hasil_str 
    except:
        hasil_display.set("Error")
        ekspresi_sekarang = ""


def ubah_persen():
    """Mengubah nilai ekspresi terakhir menjadi nilai persentase (dibagi 100)."""
    global ekspresi_sekarang
    try:
        nilai_numerik = float(eval(ekspresi_sekarang)) 
        hasil_persen = nilai_numerik / 100
        hasil_str = str(hasil_persen)

        ekspresi_sekarang = hasil_str
        hasil_display.set(format_angka(hasil_str))
    except:
        hasil_display.set("Error Persen")
        ekspresi_sekarang = ""


def ubah_tanda():
    """Mengubah tanda (+/-) dari hasil atau ekspresi."""
    global ekspresi_sekarang
    if ekspresi_sekarang and ekspresi_sekarang != '0':
        try:
            nilai = eval(ekspresi_sekarang)
            nilai_baru = -nilai
            ekspresi_sekarang = str(nilai_baru)
            hasil_display.set(format_angka(ekspresi_sekarang))
        except:
            pass


def fungsi_ilmiah(fungsi):
    """Menangani operasi ilmiah (sin, cos, sqrt, dll.)."""
    global ekspresi_sekarang
    try:
        # Hitung nilai dari ekspresi saat ini
        nilai = float(eval(ekspresi_sekarang))
        
        if fungsi == 'sqrt':
            hasil = math.sqrt(nilai)
        elif fungsi == 'sin':
            hasil = math.sin(math.radians(nilai)) # Konversi ke radian
        elif fungsi == 'cos':
            hasil = math.cos(math.radians(nilai))
        elif fungsi == 'tan':
            hasil = math.tan(math.radians(nilai))
        elif fungsi == 'log':
            hasil = math.log10(nilai)
        
        hasil_str = str(round(hasil, 10))
        ekspresi_sekarang = hasil_str
        hasil_display.set(format_angka(hasil_str))
        
    except ValueError:
        hasil_display.set("Math Error")
        ekspresi_sekarang = ""
    except:
        hasil_display.set("Error Ilmiah")
        ekspresi_sekarang = ""

# --- 3. PENGATURAN JENDELA UTAMA (GUI) ---
root = tk.Tk()
root.title("Kalkulator iOS Sederhana")
root.configure(bg=BG_UTAMA)
root.resizable(False, False)

hasil_display = tk.StringVar(value="0") 

# LAYAR TAMPILAN
layar = tk.Label(root, textvariable=hasil_display, font=('Arial', 40, 'bold'), 
                 bg=BG_UTAMA, fg=TEXT_WARNA, anchor='e', padx=15, pady=10)
layar.grid(row=0, column=0, columnspan=5, sticky='nsew', pady=(20, 10))

# --- 4. FUNGSI TOMBOL GENERIK ---

def buat_tombol(text, row, col, command_func=None, bg_warna=BTN_DARK_GREY, span=1):
    """Fungsi sederhana untuk membuat tombol dengan gaya iOS."""
    
    # Atur warna latar belakang untuk tombol Orange
    if text in ['/', '*', '-', '+', '=']:
        bg_warna = BTN_ORANGE
    # Atur warna latar belakang untuk tombol Light Grey (Fungsi)
    elif text in ['AC', 'CE', '+/-', '%']:
        bg_warna = BTN_LIGHT_GREY
        
    btn = tk.Button(root, text=text, padx=10, pady=10, bd=0, 
                    bg=bg_warna, fg=TEXT_WARNA, 
                    font=('Arial', 18), 
                    command=command_func or (lambda: tekan_tombol(text)))
    btn.grid(row=row, column=col, columnspan=span, sticky="nsew", padx=4, pady=4)
    return btn

# --- 5. TATA LETAK TOMBOL (5 KOLOM untuk Ilmiah) ---

# --- BARIS 1 (Ilmiah/Fungsi) ---
buat_tombol("AC", 1, 0, command_func=hapus_semua, bg_warna=BTN_LIGHT_GREY)
buat_tombol("+/-", 1, 1, command_func=ubah_tanda, bg_warna=BTN_LIGHT_GREY)
buat_tombol("%", 1, 2, command_func=ubah_persen, bg_warna=BTN_LIGHT_GREY)
buat_tombol("/", 1, 3, bg_warna=BTN_ORANGE)
buat_tombol("Del", 1, 4, command_func=hapus_satu_karakter, bg_warna=BTN_LIGHT_GREY)

# --- BARIS 2 ---
buat_tombol("sqrt", 2, 0, command_func=lambda: fungsi_ilmiah('sqrt'))
buat_tombol("7", 2, 1)
buat_tombol("8", 2, 2)
buat_tombol("9", 2, 3)
buat_tombol("*", 2, 4, bg_warna=BTN_ORANGE)

# --- BARIS 3 ---
buat_tombol("sin", 3, 0, command_func=lambda: fungsi_ilmiah('sin'))
buat_tombol("4", 3, 1)
buat_tombol("5", 3, 2)
buat_tombol("6", 3, 3)
buat_tombol("-", 3, 4, bg_warna=BTN_ORANGE)

# --- BARIS 4 ---
buat_tombol("cos", 4, 0, command_func=lambda: fungsi_ilmiah('cos'))
buat_tombol("1", 4, 1)
buat_tombol("2", 4, 2)
buat_tombol("3", 4, 3)
buat_tombol("+", 4, 4, bg_warna=BTN_ORANGE)

# --- BARIS 5 ---
buat_tombol("log", 5, 0, command_func=lambda: fungsi_ilmiah('log'))
buat_tombol("0", 5, 1, span=2) # Tombol 0 diperlebar
buat_tombol(".", 5, 3)
buat_tombol("=", 5, 4, command_func=hitung_hasil, bg_warna=BTN_ORANGE)


# Mengatur agar tombol melebar memenuhi jendela
for i in range(6): 
    root.grid_rowconfigure(i, weight=1)
for j in range(5): # Sekarang ada 5 kolom
    root.grid_columnconfigure(j, weight=1)

# Menjalankan aplikasi
root.mainloop()