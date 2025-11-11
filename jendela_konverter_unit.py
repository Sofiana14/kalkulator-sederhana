import tkinter as tk
from tkinter import ttk
from konstanta import *
from utilitas import adjust_font_size

# ========================== LOGIKA KONVERSI UNIT ==============================

def convert_unit(value, from_unit_name, to_unit_name, unit_data):
    """
    Melakukan konversi antar dua unit berdasarkan faktor konversi terhadap unit basis.
    unit_data adalah dictionary yang berisi semua unit dalam kategori tersebut.
    """
    if from_unit_name == to_unit_name:
        return value

    # Ambil definisi unit, abaikan metadata
    units = {name: data for name, data in unit_data.items() if name not in ('Basis', 'is_complex')}
    
    # 1. Ambil faktor untuk unit awal dan tujuan
    from_factor = units.get(from_unit_name, {}).get('factor', 1.0)
    to_factor = units.get(to_unit_name, {}).get('factor', 1.0)
    
    # --- Penanganan Konversi Khusus (Non-Linear, seperti Suhu) ---
    is_complex = unit_data.get('is_complex', False)
    
    if is_complex and unit_data['Basis'] == 'Celcius':
        # Logika Konversi Suhu
        
        # 1a. Konversi unit awal ke Celcius (basis)
        if from_unit_name == 'Fahrenheit':
            val_base = (value - 32) * 5/9
        elif from_unit_name == 'Kelvin':
            val_base = value - 273.15
        elif from_unit_name == 'Reamur':
            val_base = value * 5/4
        else: # Celcius
            val_base = value

        # 1b. Konversi dari Celcius ke unit tujuan
        if to_unit_name == 'Fahrenheit':
            result = (val_base * 9/5) + 32
        elif to_unit_name == 'Kelvin':
            result = val_base + 273.15
        elif to_unit_name == 'Reamur':
            result = val_base * 4/5
        else: # Celcius
            result = val_base
            
    # --- Konversi Linier Standar (Panjang, Massa, Volume, dll.) ---
    else:
        
        # Nilai dalam unit basis:
        value_in_base = value * from_factor
        
        # Nilai dalam unit tujuan:
        result = value_in_base / to_factor
        
    return result


# ========================== UNIT CONVERTER CLASS ==============================

class UnitConverterWindow(tk.Toplevel):
    def __init__(self, master, title, unit_data):
        super().__init__(master)
        self.title(title)
        self.configure(bg=BG_COLOR)
        # Tinggi disesuaikan untuk tombol Kembali
        self.geometry("340x580")
        self.resizable(False, False)
        
        # Sembunyikan window master (menu konverter)
        if master:
            master.withdraw()
            
        self.master = master
        self.unit_data = unit_data
        
        # Daftar nama unit yang valid (mengabaikan 'Basis' dan 'is_complex')
        self.unit_names = [name for name in unit_data if name not in ('Basis', 'is_complex')]
        
        # State: Variabel Unit yang Dipilih
        self.from_unit_name = tk.StringVar(value=self.unit_names[0])
        self.to_unit_name = tk.StringVar(value=self.unit_names[1] if len(self.unit_names) > 1 else self.unit_names[0])

        # State: Variabel Ekspresi Input/Output
        self.expression = tk.StringVar(value="0")
        # Menggunakan simbol dari unit tujuan default
        self.result_var = tk.StringVar(value=f"0 {self.get_unit_symbol(self.to_unit_name.get())}") 
        
        # --- UI Bagian Atas (Input/Output) ---
        
        # Pilihan Unit Input (Menggunakan Layout Vertikal)
        # Hapus 'from' dari pemanggilan
        self.create_unit_dropdown(self.from_unit_name).pack(anchor='w', padx=15, pady=(15, 0)) 
        
        # Label Input (font dinamis)
        self.input_label = tk.Label(self, textvariable=self.expression, font=("Segoe UI", 24), 
                                     background=BG_COLOR, foreground=FG_COLOR, justify="right", anchor='e', padx=15)
        self.input_label.pack(fill='x', padx=15)
        
        # Label simbol Unit Input
        self.from_symbol_label = tk.Label(self, text=self.get_unit_symbol(self.from_unit_name.get()), font=("Segoe UI", 10), 
                 background=BG_COLOR, foreground="#AAAAAA", justify="right", anchor='e')
        self.from_symbol_label.pack(fill='x', padx=15, pady=(0, 10))

        # Divider
        tk.Frame(self, bg=BTN_COLOR_ACCENT, height=2).pack(fill='x', padx=15, pady=5)

        # Pilihan Unit Output (Menggunakan Layout Vertikal)
        
        # Hapus 'to' dari pemanggilan
        self.create_unit_dropdown(self.to_unit_name).pack(anchor='w', padx=15, pady=(10, 0)) 
        
        # Label Output (font dinamis)
        self.output_label = tk.Label(self, textvariable=self.result_var, font=("Segoe UI", 24), 
                                     background=BG_COLOR, foreground=TEXT_COLOR, justify="right", anchor='e', padx=15)
        self.output_label.pack(fill='x', padx=15)
        
        # Label simbol Unit Output
        self.to_symbol_label = tk.Label(self, text=self.get_unit_symbol(self.to_unit_name.get()), font=("Segoe UI", 10), 
                 background=BG_COLOR, foreground="#AAAAAA", justify="right", anchor='e')
        self.to_symbol_label.pack(fill='x', padx=15, pady=(0, 15))


        # --- Keypad Kalkulator ---
        
        keypad_frame = tk.Frame(self, bg=BG_COLOR)
        keypad_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        self.create_keypad(keypad_frame)
        
        # --- Tombol Kembali ---
        self.create_back_button()
        
        # Panggil _update_result_text() setelah semua label dibuat
        self._update_result_text() 
        
        # Set protokol window closing
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # ====================================================================
        # === PERBAIKAN: DAFTARKAN TRACE SETELAH SEMUA WIDGET DIBUAT SEMUA ===
        # ====================================================================

        def _on_unit_change(unit_var, symbol_label, is_from):
            """Fungsi umum untuk menangani perubahan unit."""
            symbol_label.config(text=self.get_unit_symbol(unit_var.get()))
            self._update_conversion()
            
        # Pendaftaran trace untuk unit awal
        self.from_unit_name.trace_add("write", 
            lambda *args: _on_unit_change(self.from_unit_name, self.from_symbol_label, True))
            
        # Pendaftaran trace untuk unit tujuan
        self.to_unit_name.trace_add("write", 
            lambda *args: _on_unit_change(self.to_unit_name, self.to_symbol_label, False))

    def get_unit_symbol(self, unit_name):
        # Mengakses simbol unit dari struktur data baru
        return self.unit_data.get(unit_name, {}).get('symbol', '')

    def create_unit_dropdown(self, unit_var):
        """Membuat dropdown menu untuk memilih unit, tanpa mendaftarkan trace."""
        
        # Menentukan arah berdasarkan unit_var
        direction = 'Input' if unit_var == self.from_unit_name else 'Output'

        # Frame untuk menampung label dan dropdown
        frame = tk.Frame(self, bg=BG_COLOR)
        
        # Layout style yang diberikan
        ttk.Label(frame, text=f"Pilih Unit {direction} ▾", 
                          font=("Segoe UI", 12), background=BG_COLOR, foreground="#AAAAAA").pack(side=tk.LEFT)
                          
        # Menggunakan unit_var.get() sebagai nilai default.
        dropdown = ttk.OptionMenu(frame, unit_var, unit_var.get(), *self.unit_names)
        dropdown.config(width=15)
        dropdown.pack(side=tk.LEFT, padx=10)

        return frame

    def create_keypad(self, keypad_frame):
        buttons = [
            ('7', BTN_COLOR_NORMAL), ('8', BTN_COLOR_NORMAL), ('9', BTN_COLOR_NORMAL),
            ('4', BTN_COLOR_NORMAL), ('5', BTN_COLOR_NORMAL), ('6', BTN_COLOR_NORMAL),
            ('1', BTN_COLOR_NORMAL), ('2', BTN_COLOR_NORMAL), ('3', BTN_COLOR_NORMAL),
            ('0', BTN_COLOR_NORMAL), ('.', BTN_COLOR_NORMAL), ('', BG_COLOR), 
        ]
        
        side_buttons = [('AC', FG_COLOR), ('Del', FG_COLOR)]

        cols = 4

        # Input untuk angka (3x4)
        for i, (b_text, b_color) in enumerate(buttons):
            row_val = i // 3
            col_val = i % 3
            
            btn = tk.Button(keypad_frame, text=b_text, font=("Segoe UI", 18), 
                            bg=b_color, fg=TEXT_COLOR, bd=0, activebackground=ENTRY_BG,
                            activeforeground=TEXT_COLOR,
                            command=lambda val=b_text: self._click(val))
            
            if b_text:
                btn.grid(row=row_val, column=col_val, sticky="nsew", padx=3, pady=3, ipady=5)

        # Input untuk AC dan Del (2x1)
        btn_ac = tk.Button(keypad_frame, text=side_buttons[0][0], font=("Segoe UI", 18), 
                        bg=BTN_COLOR_ACCENT, fg=side_buttons[0][1], bd=0, activebackground=ENTRY_BG,
                        activeforeground=side_buttons[0][1],
                        command=lambda val=side_buttons[0][0]: self._click(val))
        btn_ac.grid(row=0, column=3, rowspan=2, sticky="nsew", padx=3, pady=3)

        btn_del = tk.Button(keypad_frame, text="⌫", font=("Segoe UI", 18), 
                        bg=BTN_COLOR_ACCENT, fg=side_buttons[1][1], bd=0, activebackground=ENTRY_BG,
                        activeforeground=side_buttons[1][1],
                        command=lambda val="Del": self._click(val))
        btn_del.grid(row=2, column=3, rowspan=2, sticky="nsew", padx=3, pady=3)


        for i in range(cols):
            keypad_frame.grid_columnconfigure(i, weight=1)
        for i in range(4):
            keypad_frame.grid_rowconfigure(i, weight=1)


    def _click(self, key):
        current = self.expression.get()
        if current == "0" and key.isdigit():
            self.expression.set(key)
        elif key.isdigit() or key == '.':
            if key == '.' and '.' in current:
                pass
            else:
                self.expression.set(current + key)
        elif key == "AC":
            self.expression.set("0")
        elif key == "Del":
            if len(current) > 1 and current != "0":
                self.expression.set(current[:-1])
            else:
                self.expression.set("0")
        
        adjust_font_size(self.input_label, self.expression, max_chars_small=16, max_chars_tiny=22, default_size=24)
        self._update_conversion()

    def _update_result_text(self, result=0):
        # Memformat hasil
        try:
            # Batasi hingga 10 desimal
            formatted_hasil = f"{result:.10f}".rstrip('0').rstrip('.')
            if not formatted_hasil: formatted_hasil = "0"
        except:
             formatted_hasil = "Error"
             
        symbol = self.get_unit_symbol(self.to_unit_name.get())
        self.result_var.set(f"{formatted_hasil} {symbol}")
        
        adjust_font_size(self.output_label, self.result_var, max_chars_small=16, max_chars_tiny=22, default_size=24)


    def _update_conversion(self):
        try:
            val = float(self.expression.get())
            
            hasil = convert_unit(
                val, 
                self.from_unit_name.get(), 
                self.to_unit_name.get(), 
                self.unit_data
            )
            
            self._update_result_text(hasil)

        except ValueError:
            # Nilai input tidak valid (bukan angka)
            self._update_result_text(0)
        except Exception as e:
            # Error konversi (misalnya akar negatif, log nol)
            self.result_var.set(f"Error Konversi")
            
    # --- METODE KEMBALI ---
    def create_back_button(self):
        """Membuat tombol kembali dengan style yang seragam"""
        # Frame untuk tombol kembali di bagian bawah
        button_frame = tk.Frame(self, bg=BG_COLOR)
        button_frame.pack(side="bottom", pady=(2, 10))
        
        # Tombol kembali dengan style konsisten
        back_btn = tk.Button(
            button_frame,
            text="« Kembali",
            font=("Segoe UI", 9),
            bg="#444444",
            fg=FG_COLOR,
            bd=0,
            padx=15,
            pady=6,
            command=self.on_closing,
            cursor="hand2"
        )
        back_btn.pack()
        
        # Hover effects
        back_btn.bind("<Enter>", lambda e: back_btn.configure(
            bg="#666666",
            fg=FG_COLOR
        ))
        back_btn.bind("<Leave>", lambda e: back_btn.configure(
            bg="#444444",
            fg=FG_COLOR
        ))

    def on_closing(self):
        """Handler untuk menutup window dan kembali ke menu konverter"""
        if self.master:
            self.master.deiconify()  # Tampilkan kembali menu konverter
        self.destroy()  # Tutup window konverter unit