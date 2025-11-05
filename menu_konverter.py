# menu_konverter.py

import tkinter as tk
from tkinter import ttk, messagebox
import time
from konstanta import *
from jendela_konverter_unit import UnitConverterWindow # Import dari file baru

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

        self.menu_items = [
            ("🧓", "Usia", self.konversi_usia),
            ("📏", "Area", self.konversi_area),
            ("💪", "BMI", self.konversi_bmi),
            ("💾", "Data", self.konversi_data),
            ("📅", "Tanggal", self.konversi_tanggal),
            ("🏷️", "Diskon", self.konversi_diskon),
            ("📐", "Panjang", self.konversi_panjang),
            ("⚖️", "Massa", self.konversi_massa),
            ("🔢", "Sistem angka", self.konversi_biner),
            ("🏎️", "Kecepatan", self.konversi_kecepatan),
            ("🌡️", "Suhu", self.konversi_suhu),
            ("⏰", "Waktu", self.konversi_waktu),
            ("📦", "Volume", self.konversi_volume),
            ("💰", "Mata Uang", self.konversi_uang),
            ("🔋", "Energi", self.konversi_energi),
            ("🌪️", "Tekanan", self.konversi_tekanan),
            ("🕓", "Waktu UNIX", self.konversi_unix),
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

    # ==== Fungsi Kalkulator (Popup) ====

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
                values = [float(e.get()) for e in entries]
                hasil_text = calculate_func(*values)
                result_label.config(text=hasil_text)
            except:
                messagebox.showerror("Error", "Masukkan angka yang valid")

        ttk.Button(win, text=button_text, command=hitung).pack()

    def konversi_bmi(self):
        self.calculator_popup("Hitung BMI", ["Berat (kg):", "Tinggi (cm):"], "Hitung", 
            lambda b, t: f"BMI: {round(b / ((t / 100) ** 2), 2)}")

    def konversi_diskon(self):
        self.calculator_popup("Hitung Diskon", ["Harga (Rp):", "Diskon (%):"], "Hitung", 
            lambda h, d: f"Harga Akhir: Rp {round(h - (h * d / 100), 2)}")

    def konversi_biner(self):
        self.calculator_popup("Sistem Angka", ["Masukkan angka desimal:"], "Konversi", 
            lambda n: f"Biner: {bin(int(n))[2:]}")

    def konversi_unix(self):
        self.calculator_popup("Waktu UNIX", ["Masukkan UNIX timestamp:"], "Konversi", 
            lambda t: f"Waktu: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(t)))}")

    def konversi_tanggal(self):
        messagebox.showinfo("Info", "Fitur konversi tanggal belum tersedia (dalam pengembangan).")


    # ==== Fungsi Konversi UNIT (Menggunakan UnitConverterWindow) ====
    
    def konversi_suhu(self): 
        UnitConverterWindow(self, "Konversi Suhu", {
            'from_unit': '°C', 'from_unit_name': 'Celcius', 
            'to_unit': '°F', 'to_unit_name': 'Fahrenheit', 
            'conversion_func': lambda c: (c * 9/5) + 32
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
        
    def konversi_waktu(self): 
        UnitConverterWindow(self, "Konversi Waktu", {
            'from_unit': 'j', 'from_unit_name': 'Jam', 
            'to_unit': 'm', 'to_unit_name': 'Menit', 
            'conversion_func': lambda h: h * 60
        })
        
    def konversi_data(self): 
        UnitConverterWindow(self, "Konversi Data", {
            'from_unit': 'MB', 'from_unit_name': 'Megabyte', 
            'to_unit': 'GB', 'to_unit_name': 'Gigabyte', 
            'conversion_func': lambda mb: mb / 1024
        })
        
    def konversi_kecepatan(self): 
        UnitConverterWindow(self, "Konversi Kecepatan", {
            'from_unit': 'km/j', 'from_unit_name': 'Kilometer/Jam', 
            'to_unit': 'm/d', 'to_unit_name': 'Meter/Detik', 
            'conversion_func': lambda kmh: kmh / 3.6
        })
        
    def konversi_volume(self): 
        UnitConverterWindow(self, "Konversi Volume", {
            'from_unit': 'm³', 'from_unit_name': 'Meter Kubik', 
            'to_unit': 'cm³', 'to_unit_name': 'Sentimeter Kubik', 
            'conversion_func': lambda m3: m3 * 1000000
        })
        
    def konversi_area(self): 
        UnitConverterWindow(self, "Konversi Area", {
            'from_unit': 'm²', 'from_unit_name': 'Meter Persegi', 
            'to_unit': 'cm²', 'to_unit_name': 'Sentimeter Persegi', 
            'conversion_func': lambda m2: m2 * 10000
        })
        
    def konversi_usia(self): 
        UnitConverterWindow(self, "Konversi Usia", {
            'from_unit': 't', 'from_unit_name': 'Tahun', 
            'to_unit': 'b', 'to_unit_name': 'Bulan', 
            'conversion_func': lambda th: th * 12
        })

    def konversi_uang(self):
        UnitConverterWindow(self, "Mata Uang", {
            'from_unit': 'IDR', 'from_unit_name': 'Rupiah', 
            'to_unit': 'USD', 'to_unit_name': 'Dollar AS', 
            'conversion_func': lambda idr: idr / 15500
        })

    def konversi_energi(self):
        UnitConverterWindow(self, "Energi", {
            'from_unit': 'J', 'from_unit_name': 'Joule', 
            'to_unit': 'Cal', 'to_unit_name': 'Kalori', 
            'conversion_func': lambda j: j / 4.184
        })

    def konversi_tekanan(self):
        UnitConverterWindow(self, "Tekanan", {
            'from_unit': 'Pa', 'from_unit_name': 'Pascal', 
            'to_unit': 'Bar', 'to_unit_name': 'Bar', 
            'conversion_func': lambda pa: pa / 100000
        })