import tkinter as tk
from tkinter import ttk, messagebox
import time
from datetime import date, datetime 
from konstanta import *
from jendela_konverter_unit import UnitConverterWindow 

# Menggunakan try/except untuk mengimpor kelas konverter basis angka yang telah kita buat
try:
    from jendela_konverter_basis import NumberSystemConverterWindow
except ImportError:
    NumberSystemConverterWindow = None 

# ========================== DEFINISI UNIT LENGKAP ==============================
UNIT_DEFINITIONS = {
    # 1. PANJANG (Basis: Meter)
    "Panjang": {
        'Meter': {'symbol': 'm', 'factor': 1.0},
        'Sentimeter': {'symbol': 'cm', 'factor': 0.01},
        'Kilometer': {'symbol': 'km', 'factor': 1000.0},
        'Mil': {'symbol': 'mil', 'factor': 1609.34},
        'Kaki': {'symbol': 'ft', 'factor': 0.3048},
        'Inci': {'symbol': 'in', 'factor': 0.0254},
        'Basis': 'Meter',
        # Fungsi konversi khusus untuk penanganan non-linear 
        'is_complex': False,
    },
    # 2. MASSA (Basis: Kilogram)
    "Massa": {
        'Kilogram': {'symbol': 'kg', 'factor': 1.0},
        'Gram': {'symbol': 'g', 'factor': 0.001},
        'Miligram': {'symbol': 'mg', 'factor': 0.000001},
        'Pon': {'symbol': 'lb', 'factor': 0.453592},
        'Ons': {'symbol': 'oz', 'factor': 0.02835},
        'Ton (Metrik)': {'symbol': 't', 'factor': 1000.0},
        'Basis': 'Kilogram',
        'is_complex': False,
    },
    # 3. SUHU (Basis: Celcius) 
    "Suhu": {
        'Celcius': {'symbol': '°C', 'factor': 1.0}, # Dianggap basis 1.0
        'Fahrenheit': {'symbol': '°F', 'factor': 1.0},
        'Kelvin': {'symbol': 'K', 'factor': 1.0},
        'Reamur': {'symbol': '°R', 'factor': 1.0},
        'Basis': 'Celcius',
        'is_complex': True,
    },
    # 4. VOLUME (Basis: Meter Kubik)
    "Volume": {
        'Meter Kubik': {'symbol': 'm³', 'factor': 1.0},
        'Liter': {'symbol': 'L', 'factor': 0.001},
        'Mililiter': {'symbol': 'mL', 'factor': 0.000001},
        'Galon (US)': {'symbol': 'gal', 'factor': 0.00378541},
        'Kaki Kubik': {'symbol': 'ft³', 'factor': 0.0283168},
        'Basis': 'Meter Kubik',
        'is_complex': False,
    },
    # 5. DATA (Basis: Byte)
    "Data": {
        'Byte': {'symbol': 'B', 'factor': 1.0},
        'Kilobyte': {'symbol': 'KB', 'factor': 1024.0},
        'Megabyte': {'symbol': 'MB', 'factor': 1024.0**2},
        'Gigabyte': {'symbol': 'GB', 'factor': 1024.0**3},
        'Terabyte': {'symbol': 'TB', 'factor': 1024.0**4},
        'Bit': {'symbol': 'b', 'factor': 1/8},
        'Basis': 'Byte',
        'is_complex': False,
    },
    # 6. ENERGI (Basis: Joule)
    "Energi": {
        'Joule': {'symbol': 'J', 'factor': 1.0},
        'Kalori': {'symbol': 'Cal', 'factor': 4.184},
        'Kilojoule': {'symbol': 'kJ', 'factor': 1000.0},
        'Kilokalori': {'symbol': 'kCal', 'factor': 4184.0},
        'Basis': 'Joule',
        'is_complex': False,
    },
    # 7. DAYA (Basis: Watt)
    "Daya": {
        'Watt': {'symbol': 'W', 'factor': 1.0},
        'Kilowatt': {'symbol': 'kW', 'factor': 1000.0},
        'Horsepower (metrik)': {'symbol': 'HP', 'factor': 735.499},
        'Basis': 'Watt',
        'is_complex': False,
    },
    # 8. MATA UANG 
    "Mata Uang": {
        'Rupiah': {'symbol': 'IDR', 'factor': 1.0},
        'Dollar AS': {'symbol': 'USD', 'factor': 1/15500.0}, # Nilai Statis
        'Euro': {'symbol': 'EUR', 'factor': 1/17000.0},
        'Yen Jepang': {'symbol': 'JPY', 'factor': 1/100.0},
        'Basis': 'Rupiah',
        'is_complex': False,
    },
    # 9. AREA 
    "Area": {
        'Meter Persegi': {'symbol': 'm²', 'factor': 1.0},
        'Sentimeter Persegi': {'symbol': 'cm²', 'factor': 0.0001},
        'Hektar': {'symbol': 'ha', 'factor': 10000.0},
        'Kaki Persegi': {'symbol': 'ft²', 'factor': 0.092903},
        'Basis': 'Meter Persegi',
        'is_complex': False,
    },
    # 10. KECEPATAN 
    "Kecepatan": {
        'Meter/Detik': {'symbol': 'm/s', 'factor': 1.0},
        'Kilometer/Jam': {'symbol': 'km/j', 'factor': 1/3.6},
        'Mil/Jam': {'symbol': 'mph', 'factor': 0.44704},
        'Knot': {'symbol': 'knot', 'factor': 0.514444},
        'Basis': 'Meter/Detik',
        'is_complex': False,
    },
    # 11. TEKANAN 
    "Tekanan": {
        'Pascal': {'symbol': 'Pa', 'factor': 1.0},
        'Bar': {'symbol': 'bar', 'factor': 100000.0},
        'ATM': {'symbol': 'atm', 'factor': 101325.0},
        'PSI': {'symbol': 'psi', 'factor': 6894.76},
        'Basis': 'Pascal',
        'is_complex': False,
    },
    # 12. WAKTU 
    "Waktu": {
        'Detik': {'symbol': 'd', 'factor': 1.0},
        'Menit': {'symbol': 'm', 'factor': 60.0},
        'Jam': {'symbol': 'j', 'factor': 3600.0},
        'Hari': {'symbol': 'hr', 'factor': 86400.0},
        'Tahun': {'symbol': 'th', 'factor': 31536000.0}, # Tahun kalender (365 hari)
        'Basis': 'Detik',
        'is_complex': False,
    },
    # 13. USIA
    "Usia": {
        'Tahun': {'symbol': 't', 'factor': 1.0},
        'Bulan': {'symbol': 'b', 'factor': 1/12.0},
        'Minggu': {'symbol': 'mgg', 'factor': 1/52.143},
        'Hari': {'symbol': 'hr', 'factor': 1/365.0},
        'Basis': 'Tahun',
        'is_complex': False,
    }
}


# ========================== CONVERTER MENU CLASS ==============================
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

        self.menu_items = [
            ("💪", "BMI", self.konversi_bmi), 
            ("🏷️", "Diskon", self.konversi_diskon), 
            ("📅", "Tanggal", self.konversi_tanggal), 
            ("🧓", "Usia", lambda: self.konversi_unit_umum("Usia")),
            ("📐", "Panjang", lambda: self.konversi_unit_umum("Panjang")), 
            ("⚖️", "Massa", lambda: self.konversi_unit_umum("Massa")), 
            ("🌡️", "Suhu", lambda: self.konversi_unit_umum("Suhu")), 
            ("📦", "Volume", lambda: self.konversi_unit_umum("Volume")), 
            ("💾", "Data", lambda: self.konversi_unit_umum("Data")), 
            ("🔋", "Energi", lambda: self.konversi_unit_umum("Energi")), 
            ("⚡", "Daya", lambda: self.konversi_unit_umum("Daya")), 
            ("💰", "Mata Uang", lambda: self.konversi_unit_umum("Mata Uang")), 
            ("📏", "Area", lambda: self.konversi_unit_umum("Area")), 
            ("🏎️", "Kecepatan", lambda: self.konversi_unit_umum("Kecepatan")), 
            ("🌪️", "Tekanan", lambda: self.konversi_unit_umum("Tekanan")), 
            ("⏰", "Waktu", lambda: self.konversi_unit_umum("Waktu")), 
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

    # ==== Fungsi Generik untuk Konversi Unit ====
    def konversi_unit_umum(self, category):
        """Membuka jendela konverter unit dengan semua pilihan satuan untuk kategori tertentu."""
        data = UNIT_DEFINITIONS.get(category)
        if data:
            # Mengirimkan seluruh dictionary definisi unit ke UnitConverterWindow
            UnitConverterWindow(self, f"Konversi {category}", data)
        else:
            messagebox.showerror("Error", f"Definisi unit untuk {category} tidak ditemukan.")

    # ==== Fungsi BMI (Menggunakan OptionMenu) ====

    def bmi_calculator_popup(self):
        win = tk.Toplevel(self)
        win.title("Hitung BMI Lanjut")
        win.configure(bg=BTN_COLOR_NORMAL)
        win.geometry("350x300")

        weight_var = tk.StringVar(value="")
        height_var = tk.StringVar(value="")
        weight_unit = tk.StringVar(value="Kilogram")
        height_unit = tk.StringVar(value="cm")
        
        weight_options = ["Kilogram", "Pon"]
        height_options = ["cm", "m", "Kaki", "Inci"]
        
        result_label = tk.Label(win, text="", fg=FG_COLOR, bg=BTN_COLOR_NORMAL)
        result_label.pack(pady=10)

        weight_frame = tk.Frame(win, bg=BTN_COLOR_NORMAL)
        weight_frame.pack(pady=(10, 0))
        tk.Label(weight_frame, text="Berat:", fg=TEXT_COLOR, bg=BTN_COLOR_NORMAL).pack(side=tk.LEFT)
        tk.Entry(weight_frame, textvariable=weight_var, bg=ENTRY_BG, fg=TEXT_COLOR, width=10).pack(side=tk.LEFT, padx=5)
        ttk.OptionMenu(weight_frame, weight_unit, weight_unit.get(), *weight_options).pack(side=tk.LEFT, padx=5)

        height_frame = tk.Frame(win, bg=BTN_COLOR_NORMAL)
        height_frame.pack(pady=(10, 0))
        tk.Label(height_frame, text="Tinggi:", fg=TEXT_COLOR, bg=BTN_COLOR_NORMAL).pack(side=tk.LEFT)
        tk.Entry(height_frame, textvariable=height_var, bg=ENTRY_BG, fg=TEXT_COLOR, width=10).pack(side=tk.LEFT, padx=5)
        ttk.OptionMenu(height_frame, height_unit, height_unit.get(), *height_options).pack(side=tk.LEFT, padx=5)

        def hitung():
            try:
                weight = float(weight_var.get())
                height = float(height_var.get())
                
                if weight_unit.get() == "Pon":
                    weight_kg = weight * 0.453592 
                else:
                    weight_kg = weight
                
                h_unit = height_unit.get()
                if h_unit == "cm":
                    height_m = height / 100
                elif h_unit == "Kaki":
                    height_m = height * 0.3048 
                elif h_unit == "Inci":
                    height_m = height * 0.0254 
                else: 
                    height_m = height
                
                if height_m <= 0:
                    raise ValueError("Tinggi tidak boleh nol.")

                bmi = weight_kg / (height_m ** 2)
                
                result_label.config(text=f"BMI: {round(bmi, 2)}")
                
            except ValueError:
                messagebox.showerror("Error", "Masukkan angka yang valid untuk berat dan tinggi.")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

        ttk.Button(win, text="Hitung", command=hitung).pack(pady=20)
    
    def konversi_bmi(self):
        self.bmi_calculator_popup()

    # ==== Fungsi Kalkulator Popup Generik ====

    def calculator_popup(self, title, labels, button_text, calculate_func):
        # ... (Logika calculator_popup) ...
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
                values = [e.get() for e in entries]
                hasil_text = calculate_func(*values)
                result_label.config(text=hasil_text)
            except ValueError as e:
                messagebox.showerror("Error", f"Format input salah. Detil: {e}")
            except Exception as e:
                 messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

        ttk.Button(win, text=button_text, command=hitung).pack()

    # --- IMPLEMENTASI FITUR POPUP ---

    def konversi_diskon(self):
        self.calculator_popup("Hitung Diskon", ["Harga (Rp):", "Diskon (%):"], "Hitung", 
            lambda h, d: f"Harga Akhir: Rp {round(float(h) - (float(h) * float(d) / 100), 2)}")

    def konversi_unix(self):
        self.calculator_popup("Waktu UNIX", ["Masukkan UNIX timestamp:"], "Konversi", 
            lambda t: f"Waktu: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(t)))}")

    def konversi_tanggal(self):
        def hitung_selisih_tanggal(tgl_awal_str, tgl_akhir_str):
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