import tkinter as tk
from tkinter import ttk, messagebox
import time
from datetime import date, datetime # Diperlukan untuk konversi Tanggal
from konstanta import *
from jendela_konverter_unit import UnitConverterWindow 

# Menggunakan try/except untuk mengimpor kelas konverter basis angka yang telah kita buat
try:
    from jendela_konverter_basis import NumberSystemConverterWindow
except ImportError:
    # Jika file belum ada, set ke None dan berikan error info saat dipanggil
    NumberSystemConverterWindow = None 

# ========================== CONVERTER MENU ==============================
class ConverterUI(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Menu Konverter")
        self.configure(bg=BG_COLOR)
        self.geometry("380x680")
        self.resizable(True, True) 

        title = tk.Label(self, text="Converter", fg=FG_COLOR, bg=BG_COLOR,
                         font=("Segoe UI", 16, "bold"))
        title.pack(pady=15)

        grid_frame = tk.Frame(self, bg=BG_COLOR)
        grid_frame.pack(pady=(10, 0)) 

        # Daftar item menu yang sudah lengkap
        self.menu_items = [
            ("💪", "BMI", self.konversi_bmi), 
            ("🏷️", "Diskon", self.konversi_diskon), 
            ("📅", "Tanggal", self.konversi_tanggal), 
            ("🧓", "Usia", self.konversi_usia), 
            ("📐", "Panjang", self.konversi_panjang), 
            ("⚖️", "Massa", self.konversi_massa), 
            ("🌡️", "Suhu", self.konversi_suhu), 
            ("📦", "Volume", self.konversi_volume), 
            ("💾", "Data", self.konversi_data), 
            ("🔋", "Energi", self.konversi_energi), 
            ("⚡", "Daya", self.konversi_daya), 
            ("💰", "Mata Uang", self.konversi_uang), 
            ("📏", "Area", self.konversi_area), 
            ("🏎️", "Kecepatan", self.konversi_kecepatan), 
            ("🌪️", "Tekanan", self.konversi_tekanan), 
            ("⏰", "Waktu", self.konversi_waktu), 
            ("🕓", "Waktu UNIX", self.konversi_unix), 
            ("🔢", "Basis Angka", self.konversi_basis_angka), 
        ]

        cols = 3
        for i, (icon, name, func) in enumerate(self.menu_items):
            frame = tk.Frame(grid_frame, bg=BG_COLOR)
            frame.grid(row=i // cols, column=i % cols, padx=15, pady=20)

            label_icon = tk.Label(frame, text=icon, fg=TEXT_COLOR, bg=BG_COLOR, font=("Segoe UI Emoji", 22))
            label_icon.pack()

            btn = tk.Button(frame, text=name, fg="#AAAAAA", bg=BG_COLOR,
                            font=("Segoe UI", 9), bd=0, activebackground=BTN_COLOR_NORMAL,
                            activeforeground=FG_COLOR, command=func)
            btn.pack()

        ttk.Button(self, text="Kembali", command=self.destroy).pack(pady=20) 

    # ==== Fungsi Kalkulator Popup (Formula/Simple) ====

    def calculator_popup(self, title, labels, button_text, calculate_func):
        win = tk.Toplevel(self)
        win.title(title)
        win.configure(bg=BTN_COLOR_NORMAL)
        win.geometry("300x300")
        
        entries = []
        
        for label_text in labels:
            tk.Label(win, text=label_text, fg=TEXT_COLOR, bg=BTN_COLOR_NORMAL).pack(pady=(10, 0))
            entry = tk.Entry(win, bg=ENTRY_BG, fg=TEXT_COLOR)
            entry.pack(pady=(0, 5))
            entries.append(entry)
            
        result_label = tk.Label(win, text="", fg=FG_COLOR, bg=BTN_COLOR_NORMAL)
        result_label.pack(pady=10)

        def hitung():
            try:
                # Ambil semua input sebagai string
                values = [e.get() for e in entries]
                
                # Fungsi calculate_func harus menangani input string (khusus untuk tanggal)
                # Untuk BMI/Diskon, nilai akan diubah menjadi float di dalam calculate_func
                hasil_text = calculate_func(*values)
                result_label.config(text=hasil_text)
            except ValueError as e:
                messagebox.showerror("Error", f"Format input salah. Detil: {e}")
            except Exception as e:
                 messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

        ttk.Button(win, text=button_text, command=hitung).pack()

    # --- IMPLEMENTASI FITUR POPUP ---

    def konversi_bmi(self):
        # Input dari user dalam cm, formula butuh meter
        self.calculator_popup("Hitung BMI", ["Berat (kg):", "Tinggi (cm):"], "Hitung", 
            lambda b, t: f"BMI: {round(float(b) / ((float(t) / 100) ** 2), 2)}")

    def konversi_diskon(self):
        # Harga Akhir = Harga Awal - (Harga Awal * Diskon %)
        self.calculator_popup("Hitung Diskon", ["Harga (Rp):", "Diskon (%):"], "Hitung", 
            lambda h, d: f"Harga Akhir: Rp {round(float(h) - (float(h) * float(d) / 100), 2)}")

    def konversi_unix(self):
        self.calculator_popup("Waktu UNIX", ["Masukkan UNIX timestamp:"], "Konversi", 
            lambda t: f"Waktu: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(t)))}")

    def konversi_tanggal(self):
        def hitung_selisih_tanggal(tgl_awal_str, tgl_akhir_str):
            # Format: YYYY-MM-DD
            tgl_awal = datetime.strptime(tgl_awal_str, '%Y-%m-%d').date()
            tgl_akhir = datetime.strptime(tgl_akhir_str, '%Y-%m-%d').date()
            
            selisih = abs((tgl_akhir - tgl_awal).days)
            
            return f"Selisih: {selisih} hari"

        self.calculator_popup("Konversi Tanggal", 
            ["Tanggal Awal (YYYY-MM-DD):", "Tanggal Akhir (YYYY-MM-DD):"], 
            "Hitung Selisih", 
            hitung_selisih_tanggal)
            
    def konversi_basis_angka(self):
         if NumberSystemConverterWindow:
            NumberSystemConverterWindow(self)
         else:
             messagebox.showerror("Error", "Kelas 'NumberSystemConverterWindow' (dari jendela_konverter_basis.py) tidak ditemukan.")

    # ==== Fungsi Konversi UNIT (Menggunakan UnitConverterWindow) ====
    
    def konversi_usia(self): 
        UnitConverterWindow(self, "Konversi Usia", {
            'from_unit': 't', 'from_unit_name': 'Tahun', 
            'to_unit': 'b', 'to_unit_name': 'Bulan', 
            'conversion_func': lambda th: th * 12
        })

    def konversi_panjang(self): 
        UnitConverterWindow(self, "Konversi Panjang", {
            'from_unit': 'm', 'from_unit_name': 'Meter', 
            'to_unit': 'cm', 'to_unit_name': 'Sentimeter', 
            'conversion_func': lambda m: m * 100
        })
    
    def konversi_massa(self): 
        UnitConverterWindow(self, "Konversi Massa", {
            'from_unit': 'kg', 'from_unit_name': 'Kilogram', 
            'to_unit': 'g', 'to_unit_name': 'Gram', 
            'conversion_func': lambda kg: kg * 1000
        })

    def konversi_suhu(self): 
        UnitConverterWindow(self, "Konversi Suhu", {
            'from_unit': '°C', 'from_unit_name': 'Celcius', 
            'to_unit': '°F', 'to_unit_name': 'Fahrenheit', 
            'conversion_func': lambda c: (c * 9/5) + 32
        })
        
    def konversi_volume(self): 
        UnitConverterWindow(self, "Konversi Volume", {
            'from_unit': 'm³', 'from_unit_name': 'Meter Kubik', 
            'to_unit': 'L', 'to_unit_name': 'Liter', 
            'conversion_func': lambda m3: m3 * 1000
        })

    def konversi_data(self): 
        UnitConverterWindow(self, "Konversi Data", {
            'from_unit': 'MB', 'from_unit_name': 'Megabyte', 
            'to_unit': 'GB', 'to_unit_name': 'Gigabyte', 
            'conversion_func': lambda mb: mb / 1024
        })

    def konversi_energi(self):
        UnitConverterWindow(self, "Energi", {
            'from_unit': 'J', 'from_unit_name': 'Joule', 
            'to_unit': 'Cal', 'to_unit_name': 'Kalori', 
            'conversion_func': lambda j: j / 4.184
        })
        
    def konversi_daya(self):
        UnitConverterWindow(self, "Konversi Daya", {
            'from_unit': 'kW', 'from_unit_name': 'Kilowatt', 
            'to_unit': 'HP', 'to_unit_name': 'Horsepower', 
            'conversion_func': lambda kw: kw * 1.341
        })

    def konversi_uang(self):
        UnitConverterWindow(self, "Mata Uang (Contoh)", {
            'from_unit': 'IDR', 'from_unit_name': 'Rupiah', 
            'to_unit': 'USD', 'to_unit_name': 'Dollar AS', 
            'conversion_func': lambda idr: idr / 15500
        })

    def konversi_area(self): 
        UnitConverterWindow(self, "Konversi Area", {
            'from_unit': 'm²', 'from_unit_name': 'Meter Persegi', 
            'to_unit': 'cm²', 'to_unit_name': 'Sentimeter Persegi', 
            'conversion_func': lambda m2: m2 * 10000
        })

    def konversi_kecepatan(self): 
        UnitConverterWindow(self, "Konversi Kecepatan", {
            'from_unit': 'km/j', 'from_unit_name': 'Kilometer/Jam', 
            'to_unit': 'm/d', 'to_unit_name': 'Meter/Detik', 
            'conversion_func': lambda kmh: kmh / 3.6
        })

    def konversi_tekanan(self):
        UnitConverterWindow(self, "Tekanan", {
            'from_unit': 'Pa', 'from_unit_name': 'Pascal', 
            'to_unit': 'Bar', 'to_unit_name': 'Bar', 
            'conversion_func': lambda pa: pa / 100000
        })

    def konversi_waktu(self): 
        UnitConverterWindow(self, "Konversi Waktu", {
            'from_unit': 'j', 'from_unit_name': 'Jam', 
            'to_unit': 'm', 'to_unit_name': 'Menit', 
            'conversion_func': lambda h: h * 60
        })