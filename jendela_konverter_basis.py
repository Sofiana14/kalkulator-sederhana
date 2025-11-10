import tkinter as tk
from tkinter import ttk
from konstanta import *
from utilitas import adjust_font_size
import re

# ========================== UNIT CONVERTER CLASS ==============================

class NumberSystemConverterWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Konverter Basis Angka")
        self.configure(bg=BG_COLOR)
        self.geometry("340x580")  # Ukuran disesuaikan untuk tombol kembali
        self.resizable(False, False)
        
        # Simpan referensi ke master window
        self.master = master
        
        # Tambahkan tombol kembali di bagian bawah
        self.create_back_button()
        
        # Basis Angka yang Tersedia
        self.bases = {
            'Desimal (Dec)': 10,
            'Biner (Bin)': 2,
            'Oktal (Oct)': 8,
            'Heksadesimal (Hex)': 16
        }
        self.base_names = list(self.bases.keys())
        
        # Variabel State
        self.from_base_name = tk.StringVar(value=self.base_names[0]) # Default: Desimal
        self.expression = tk.StringVar(value="0")
        
        # Hasil konversi untuk setiap basis (Dec, Bin, Oct, Hex)
        self.results = {name: tk.StringVar(value="0") for name in self.base_names}
        
        # Panggil UI
        self._create_ui()
        self._update_conversion(initial=True)
        
    def _create_ui(self):
        # --- UI Bagian Atas (Input) ---
        
        # Pilihan Basis Input
        from_base_frame = tk.Frame(self, bg=BG_COLOR)
        from_base_frame.pack(anchor='w', padx=15, pady=(15, 0))
        
        ttk.Label(from_base_frame, text="Basis Input ▾", font=("Segoe UI", 12), 
                  background=BG_COLOR, foreground="#AAAAAA").pack(side=tk.LEFT)
                  
        self.base_option_menu = ttk.OptionMenu(from_base_frame, self.from_base_name, 
                                               self.from_base_name.get(), 
                                               *self.base_names, 
                                               command=self._on_base_change)
        self.base_option_menu.config(width=15)
        self.base_option_menu.pack(side=tk.LEFT, padx=10)

        # Label Input (font dinamis)
        self.input_label = tk.Label(self, textvariable=self.expression, font=("Segoe UI", 24), 
                                    background=BG_COLOR, foreground=FG_COLOR, 
                                    justify="right", anchor='e', padx=15)
        self.input_label.pack(padx=15, pady=(5, 15), fill="x", ipady=10)
        
        # --- UI Bagian Tengah (Output Hasil) ---
        
        result_frame = tk.Frame(self, bg=BG_COLOR)
        result_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # Tampilkan semua hasil konversi
        for name, var in self.results.items():
            tk.Label(result_frame, text=name, font=("Segoe UI", 10), 
                     bg=BG_COLOR, fg="#AAAAAA", anchor='w').pack(fill='x')
            tk.Label(result_frame, textvariable=var, font=("Segoe UI", 14, "bold"), 
                     bg=BG_COLOR, fg=TEXT_COLOR, anchor='e', pady=2).pack(fill='x')
            ttk.Separator(result_frame, orient='horizontal').pack(fill='x', pady=(0, 5))

        # --- UI Bagian Bawah (Keypad) ---
        
        keypad_frame = tk.Frame(self, bg=BG_COLOR)
        keypad_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        self._create_keypad(keypad_frame)

    def _on_base_change(self, *args):
        # Reset input dan update keypad saat basis input berubah
        self.expression.set("0")
        self._create_keypad(self.winfo_children()[-1])
        self._update_conversion(initial=True)
        
    def _create_keypad(self, keypad_frame):
        # Hapus tombol lama sebelum membuat yang baru
        for widget in keypad_frame.winfo_children():
            widget.destroy()

        current_base = self.bases[self.from_base_name.get()]
        
        # Tombol-tombol heksadesimal
        hex_buttons = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F')]
        
        # Tombol standar untuk kalkulator basis
        num_buttons = [
            ('AC', BTN_COLOR_ACCENT), ('Del', BTN_COLOR_ACCENT), 
            ('7', BTN_COLOR_NORMAL), ('8', BTN_COLOR_NORMAL), ('9', BTN_COLOR_NORMAL), 
            ('4', BTN_COLOR_NORMAL), ('5', BTN_COLOR_NORMAL), ('6', BTN_COLOR_NORMAL), 
            ('1', BTN_COLOR_NORMAL), ('2', BTN_COLOR_NORMAL), ('3', BTN_COLOR_NORMAL), 
            ('0', BTN_COLOR_NORMAL), ('.', BTN_COLOR_NORMAL)
        ]
        
        # Tambahkan tombol heksa jika basisnya adalah 16
        if current_base == 16:
            for text, val in hex_buttons:
                num_buttons.insert(0, (text, BTN_COLOR_NORMAL))
        
        # Filter tombol berdasarkan basis saat ini
        valid_keys = set([str(i) for i in range(current_base)] + ['AC', 'Del', '.', *[h[0] for h in hex_buttons]])
        filtered_buttons = [btn for btn in num_buttons if btn[0] in valid_keys]
        
        cols = 5 
        
        # Layout Tombol
        row_map = {
            'AC': (0, 3), 'Del': (0, 4), 'A': (1, 0), 'B': (1, 1), 'C': (1, 2),
            '7': (2, 0), '8': (2, 1), '9': (2, 2), 'D': (2, 3), 'E': (2, 4),
            '4': (3, 0), '5': (3, 1), '6': (3, 2), 'F': (3, 3), 
            '1': (4, 0), '2': (4, 1), '3': (4, 2), 
            '0': (5, 0), '.': (5, 1) # Desimal tidak didukung untuk basis lain
        }
        
        for i in range(cols):
            keypad_frame.grid_columnconfigure(i, weight=1)
        for i in range(6): 
            keypad_frame.grid_rowconfigure(i, weight=1)
            
        col_offset = 0 # Digunakan untuk angka 7-9 dst jika tombol heksa ada

        for b_text, b_color in filtered_buttons:
            
            # Khusus untuk heksadesimal
            if current_base == 16 and b_text in ['A', 'B', 'C', 'D', 'E', 'F']:
                row_val, col_val = row_map[b_text]
                
            # Logika tata letak untuk angka (0-9)
            elif b_text.isdigit():
                # Jika heksa aktif, angka 7-9 bergeser
                if current_base == 16 and int(b_text) >= 7:
                    if int(b_text) in [7, 8, 9]:
                        row_val, col_val = 2, int(b_text) - 7
                    elif int(b_text) in [4, 5, 6]:
                        row_val, col_val = 3, int(b_text) - 4
                    elif int(b_text) in [1, 2, 3]:
                        row_val, col_val = 4, int(b_text) - 1
                    else: # 0
                        row_val, col_val = 5, 0
                
                # Tata letak standar (Dec, Oct, Bin)
                else:
                    if int(b_text) in [7, 8, 9]:
                        row_val, col_val = 1, int(b_text) - 7 + 2 # +2 karena kolom 0 dan 1 untuk AC/DEL
                    elif int(b_text) in [4, 5, 6]:
                        row_val, col_val = 2, int(b_text) - 4 + 2
                    elif int(b_text) in [1, 2, 3]:
                        row_val, col_val = 3, int(b_text) - 1 + 2
                    elif b_text == '0':
                        row_val, col_val = 4, 3
                    else:
                        continue # Skip angka lain
                        
            # AC/Del
            elif b_text in ['AC', 'Del']:
                 row_val, col_val = row_map[b_text]

            # Tombol yang dinonaktifkan
            elif b_text == '.':
                if current_base != 10: continue
                row_val, col_val = 5, 1
            
            else:
                continue

            # Konfigurasi tombol
            btn_bg = b_color
            btn_fg = FG_COLOR if b_color == BTN_COLOR_ACCENT else TEXT_COLOR

            # Tombol akan dinonaktifkan jika tidak valid untuk basis saat ini
            is_valid = True
            if current_base < 16 and b_text in ['A', 'B', 'C', 'D', 'E', 'F']:
                is_valid = False
            if current_base <= 8 and b_text in ['8', '9']:
                is_valid = False
            if current_base <= 2 and b_text in ['2', '3', '4', '5', '6', '7', '8', '9']:
                is_valid = False

            btn = tk.Button(keypad_frame, text=b_text, font=("Segoe UI", 14), 
                            bg=btn_bg, fg=btn_fg, bd=0, 
                            activebackground=ENTRY_BG, activeforeground=btn_fg,
                            command=lambda val=b_text: self._click(val))
                            
            if not is_valid:
                # Menonaktifkan tombol yang tidak valid secara visual
                btn.config(state=tk.DISABLED, bg="#333333", fg="#AAAAAA")

            
            # Tata letak tombol
            if b_text == 'AC':
                btn.grid(row=row_val, column=col_val, columnspan=2, sticky="nsew", padx=3, pady=3)
            elif b_text == '0':
                btn.grid(row=row_val, column=col_val, columnspan=3, sticky="nsew", padx=3, pady=3)
            else:
                btn.grid(row=row_val, column=col_val, sticky="nsew", padx=3, pady=3)


        # Menambahkan tombol sisa di kolom 3 dan 4 (Del, dsb)
        
        # AC dan DEL
        btn_ac = tk.Button(keypad_frame, text="AC", font=("Segoe UI", 18), 
                            bg=BTN_COLOR_ACCENT, fg=FG_COLOR, bd=0, activebackground=ENTRY_BG,
                            activeforeground=FG_COLOR,
                            command=lambda val="AC": self._click(val))
        btn_ac.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

        btn_del = tk.Button(keypad_frame, text="⌫", font=("Segoe UI", 18), 
                            bg=BTN_COLOR_ACCENT, fg=FG_COLOR, bd=0, activebackground=ENTRY_BG,
                            activeforeground=FG_COLOR,
                            command=lambda val="Del": self._click(val))
        btn_del.grid(row=0, column=2, columnspan=3, sticky="nsew", padx=3, pady=3)
        

    def _click(self, key):
        curr = self.expression.get()
        current_base = self.bases[self.from_base_name.get()]
        
        if key == "AC":
            self.expression.set("0")
        elif key == "Del":
            if curr == "0" or len(curr) <= 1:
                self.expression.set("0")
            else:
                self.expression.set(curr[:-1])
        else:
            if curr == "0":
                if key == '.': # Jika input . pertama kali
                    self.expression.set("0" + key)
                else:
                    self.expression.set(key)
            else:
                # Cegah lebih dari satu titik desimal, hanya untuk basis 10
                if key == '.' and ('.' in curr or current_base != 10):
                    return
                self.expression.set(curr + key)
                
        self._update_conversion()
        
        adjust_font_size(self.input_label, self.expression, max_chars_small=12, max_chars_tiny=18, default_size=24)

    def _update_conversion(self, initial=False):
        input_str = self.expression.get()
        from_base_name = self.from_base_name.get()
        from_base = self.bases[from_base_name]

        try:
            # Hanya desimal yang mendukung pecahan, jadi kita hanya ambil bagian integer
            if '.' in input_str and from_base == 10:
                decimal_val = float(input_str)
                integer_val = int(decimal_val)
            elif '.' in input_str and from_base != 10:
                # Basis lain tidak mendukung pecahan, tampilkan error atau gunakan bagian integer
                raise ValueError("Basis non-desimal tidak mendukung pecahan.")
            elif input_str.strip() == "":
                 integer_val = 0
            else:
                integer_val = int(input_str, from_base) # Konversi ke integer desimal
            
            # --- Konversi ---
            
            # Desimal (Dec)
            self.results[self.base_names[0]].set(str(integer_val))
            
            # Biner (Bin)
            self.results[self.base_names[1]].set(bin(integer_val)[2:])
            
            # Oktal (Oct)
            self.results[self.base_names[2]].set(oct(integer_val)[2:])
            
            # Heksadesimal (Hex)
            self.results[self.base_names[3]].set(hex(integer_val)[2:].upper())
            
        except ValueError as e:
            # Tangani error seperti input invalid (misalnya 'A' di mode Desimal)
            error_msg = "Input Tidak Valid"
            if initial:
                 error_msg = "0"

            for name in self.base_names:
                self.results[name].set(error_msg)
        except Exception:
            for name in self.base_names:
                self.results[name].set("Error")

    def create_back_button(self):
        """Membuat tombol kembali dengan style yang seragam"""
        # Frame untuk tombol kembali di bagian bawah
        button_frame = tk.Frame(self, bg=BG_COLOR)
        button_frame.pack(side="bottom", pady=(10, 15))
        
        # Tombol kembali dengan style konsisten
        back_btn = tk.Button(
            button_frame,
            text="« Kembali",
            font=("Segoe UI", 10),
            bg=BTN_COLOR_ACCENT,
            fg=FG_COLOR,
            bd=0,
            padx=20,
            pady=8,
            command=self.on_closing,
            cursor="hand2"
        )
        back_btn.pack()
        
        # Hover effects
        back_btn.bind("<Enter>", lambda e: back_btn.configure(
            bg=FG_COLOR,
            fg=BG_COLOR
        ))
        back_btn.bind("<Leave>", lambda e: back_btn.configure(
            bg=BTN_COLOR_ACCENT,
            fg=FG_COLOR
        ))

    def on_closing(self):
        """Handler untuk menutup window dan kembali ke menu konverter"""
        self.master.deiconify()  # Tampilkan kembali menu konverter
        self.destroy()  # Tutup window konverter

# Fungsi untuk membuka jendela dari menu utama
def open_number_system_converter(root):
    NumberSystemConverterWindow(root)