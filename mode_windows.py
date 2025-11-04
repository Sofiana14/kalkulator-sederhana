# mode_windows.py

import tkinter as tk
from tkinter import ttk, messagebox
import time, math
from calculator_logic import evaluate_expression, calculate_function
from constants import *
import re 

# ========================== FUNGSI UTILITAS FONT DINAMIS ==========================
def adjust_font_size(widget, text_var, max_chars_small, max_chars_tiny, default_size):
    """Menyesuaikan ukuran font pada widget berdasarkan panjang string."""
    text_length = len(text_var.get())
    
    # Menentukan ukuran font berdasarkan panjang teks
    if text_length > max_chars_tiny:
        new_size = 14 
    elif text_length > max_chars_small:
        new_size = 18 
    else:
        new_size = default_size 

    # Menerapkan font hanya jika ukurannya berubah
    current_font_spec = widget.cget("font")
    try:
        current_size = int(re.search(r'\d+', current_font_spec).group(0))
    except:
        current_size = default_size 

    if current_size != new_size:
        widget.config(font=("Segoe UI", new_size))
        
# ========================== BASIC CALCULATOR ==============================
def open_basic_calculator(root):
    win = tk.Toplevel(root)
    win.title("Kalkulator Dasar")
    win.geometry("340x500") 
    win.configure(bg=BG_COLOR)
    win.resizable(False, False)

    expression = tk.StringVar()
    expression.set("0")

    entry = tk.Label(win, textvariable=expression, font=("Segoe UI", 28),
                     bg=ENTRY_BG, fg=TEXT_COLOR, justify="right", anchor='e',
                     bd=0, relief=tk.FLAT, padx=10)
    entry.pack(padx=10, pady=(20, 10), fill="x", ipady=10)

    buttons = [
        ('AC', BTN_COLOR_ACCENT), ('Del', BTN_COLOR_ACCENT), ('(', BTN_COLOR_ACCENT), (')', BTN_COLOR_ACCENT), ('/', BTN_COLOR_ACCENT),
        ('7', BTN_COLOR_NORMAL), ('8', BTN_COLOR_NORMAL), ('9', BTN_COLOR_NORMAL), ('*', BTN_COLOR_ACCENT), ('%', BTN_COLOR_ACCENT),
        ('4', BTN_COLOR_NORMAL), ('5', BTN_COLOR_NORMAL), ('6', BTN_COLOR_NORMAL), ('-', BTN_COLOR_ACCENT), ('sqrt', BTN_COLOR_ACCENT),
        ('1', BTN_COLOR_NORMAL), ('2', BTN_COLOR_NORMAL), ('3', BTN_COLOR_NORMAL), ('+', BTN_COLOR_ACCENT), ('=', BG_COLOR),
        ('0', BTN_COLOR_NORMAL), ('.', BTN_COLOR_NORMAL), ('00', BTN_COLOR_NORMAL), ('^', BTN_COLOR_ACCENT), ('log', BTN_COLOR_ACCENT)
    ]

    def click(key):
        current_expression = expression.get()
        
        if current_expression == "0" and key.isdigit():
            expression.set(key)
        elif key == "=":
            result = evaluate_expression(current_expression)
            expression.set(str(result))
        elif key == "AC":
            expression.set("0")
        elif key == "Del":
            if len(current_expression) > 1 and current_expression != "0":
                expression.set(current_expression[:-1])
            else:
                expression.set("0")
        elif key in ('sqrt', 'log'): 
            # Handle kasus saat '0' diikuti oleh fungsi
            if current_expression == "0":
                expression.set(key + '(')
            else:
                expression.set(current_expression + key + '(')
        elif key == '%':
            try:
                result = evaluate_expression(current_expression.replace('%', '/100'))
                expression.set(str(result))
            except Exception:
                expression.set("Error")
        else:
            if current_expression == "0":
                current_expression = ""
            expression.set(current_expression + key)
        
        adjust_font_size(entry, expression, max_chars_small=14, max_chars_tiny=20, default_size=28)


    button_frame = tk.Frame(win, bg=BG_COLOR)
    button_frame.pack(expand=True, fill="both", padx=5, pady=5)
    
    cols = 5
    for i, (b_text, b_color) in enumerate(buttons):
        row_val = i // cols
        col_val = i % cols
        
        if b_text == '=':
            btn_bg = FG_COLOR 
            btn_fg = BG_COLOR
        elif b_color == BTN_COLOR_ACCENT:
            btn_bg = BTN_COLOR_ACCENT
            btn_fg = FG_COLOR
        else:
            btn_bg = BTN_COLOR_NORMAL
            btn_fg = TEXT_COLOR
            
        btn = tk.Button(button_frame, text=b_text, font=("Segoe UI", 14), 
                      bg=btn_bg, fg=btn_fg, bd=0, activebackground=ENTRY_BG,
                      activeforeground=TEXT_COLOR,
                      command=lambda val=b_text: click(val))
        
        btn.grid(row=row_val, column=col_val, sticky="nsew", padx=3, pady=3, ipady=5)

    for i in range(cols):
        button_frame.grid_columnconfigure(i, weight=1)
    for i in range(len(buttons) // cols + 1):
        button_frame.grid_rowconfigure(i, weight=1)

# ========================== FUNCTION CALCULATOR ==============================
def open_function_calculator(root):
    win = tk.Toplevel(root)
    win.title("Kalkulator Fungsi Lanjut")
    win.geometry("380x600") # Ukuran disesuaikan untuk lebih banyak tombol
    win.configure(bg=BG_COLOR)
    win.resizable(True, True) # Bisa diresize

    expression_history = tk.StringVar(value="") # Untuk menampilkan riwayat ekspresi
    current_expression = tk.StringVar(value="0") # Untuk ekspresi yang sedang diketik
    
    # Area tampilan riwayat ekspresi (lebih kecil)
    history_label = tk.Label(win, textvariable=expression_history, font=("Segoe UI", 16),
                             bg=BG_COLOR, fg="#AAAAAA", justify="right", anchor='e',
                             bd=0, relief=tk.FLAT, padx=10, pady=5)
    history_label.pack(padx=10, pady=(15, 0), fill="x")

    # Area tampilan ekspresi utama (lebih besar dan dinamis)
    entry_label = tk.Label(win, textvariable=current_expression, font=("Segoe UI", 32),
                           bg=BG_COLOR, fg=FG_COLOR, justify="right", anchor='e',
                           bd=0, relief=tk.FLAT, padx=10, pady=5)
    entry_label.pack(padx=10, pady=(0, 15), fill="x")

    # --- Click Handler untuk Kalkulator Fungsi ---
    def click(key):
        hist = expression_history.get()
        curr = current_expression.get()

        if key == "AC":
            current_expression.set("0")
            expression_history.set("")
        elif key == "Del":
            if curr == "Error" or curr == "Invalid Input":
                current_expression.set("0")
            elif len(curr) > 1 and curr != "0":
                current_expression.set(curr[:-1])
            else:
                current_expression.set("0")
        elif key == "=":
            try:
                # Ganti simbol matematika agar dapat dievaluasi oleh evaluate_expression
                display_expr = curr.replace('^', '**').replace('x', '*')
                
                # Mengubah fungsi untuk evaluasi yang benar
                # Cek dulu apakah ada pi atau e yang belum diubah menjadi nilai float
                display_expr = display_expr.replace('π', str(math.pi)).replace('e', str(math.e))
                
                # Fungsi log dan sqrt perlu diubah ke format math.log atau math.sqrt
                # Pastikan tidak mengganti 'log' di dalam 'log10'
                display_expr = re.sub(r'log(\()', r'math.log10\1', display_expr) 
                display_expr = re.sub(r'ln(\()', r'math.log\1', display_expr) # ln adalah log natural (basis e)
                display_expr = re.sub(r'sqrt(\()', r'math.sqrt\1', display_expr)
                display_expr = re.sub(r'sin(\()', r'math.sin(math.radians(', display_expr) # default radian
                display_expr = re.sub(r'cos(\()', r'math.cos(math.radians(', display_expr) # default radian
                display_expr = re.sub(r'tan(\()', r'math.tan(math.radians(', display_expr) # default radian
                
                if 'math.radians(' in display_expr: # Tutup kurung untuk math.radians jika ada
                    display_expr += '))' # Tambah penutup untuk radians dan fungsi

                result = evaluate_expression(display_expr)
                expression_history.set(curr + "=")
                current_expression.set(str(result))
            except Exception as e:
                current_expression.set("Error")
                expression_history.set("")
        else:
            if curr == "0" or curr == "Error" or curr == "Invalid Input":
                # Jika input pertama adalah operator atau simbol, tambahkan ke 0
                if key in ('+', '-', '*', '/', '^', '%', 'x!'):
                    current_expression.set(curr + key)
                elif key in ('sin(', 'cos(', 'tan(', 'log(', 'sqrt(', 'ln(', 'lg(', 'π', 'e'):
                    current_expression.set(key) # Ganti "0" dengan fungsi/konstanta
                else:
                    current_expression.set(key)
            else:
                current_expression.set(curr + key)
        
        # Panggil penyesuaian font untuk ekspresi utama
        adjust_font_size(entry_label, current_expression, max_chars_small=12, max_chars_tiny=18, default_size=32)

    # --- Frame untuk tombol kalkulator ---
    button_frame = tk.Frame(win, bg=BG_COLOR)
    button_frame.pack(expand=True, fill="both", padx=5, pady=5)
    
    # Tombol-tombol untuk kalkulator fungsi (disesuaikan dengan gambar)
    # Beberapa operator akan dihandle secara khusus di click function
    buttons = [
        # Baris 1
        ('2nd', BTN_COLOR_NORMAL, TEXT_COLOR), ('deg', BTN_COLOR_NORMAL, TEXT_COLOR), ('sin', BTN_COLOR_NORMAL, TEXT_COLOR), ('cos', BTN_COLOR_NORMAL, TEXT_COLOR), ('tan', BTN_COLOR_NORMAL, TEXT_COLOR),
        # Baris 2
        ('x^y', BTN_COLOR_NORMAL, TEXT_COLOR), ('lg', BTN_COLOR_NORMAL, TEXT_COLOR), ('ln', BTN_COLOR_NORMAL, TEXT_COLOR), ('(', BTN_COLOR_ACCENT, FG_COLOR), (')', BTN_COLOR_ACCENT, FG_COLOR),
        # Baris 3
        ('sqrt', BTN_COLOR_NORMAL, TEXT_COLOR), ('AC', BTN_COLOR_ACCENT, FG_COLOR), ('Del', BTN_COLOR_ACCENT, FG_COLOR), ('%', BTN_COLOR_ACCENT, FG_COLOR), ('/', BTN_COLOR_ACCENT, FG_COLOR),
        # Baris 4
        ('x!', BTN_COLOR_NORMAL, TEXT_COLOR), ('7', BTN_COLOR_NORMAL, TEXT_COLOR), ('8', BTN_COLOR_NORMAL, TEXT_COLOR), ('9', BTN_COLOR_NORMAL, TEXT_COLOR), ('x', BTN_COLOR_ACCENT, FG_COLOR),
        # Baris 5
        ('1/x', BTN_COLOR_NORMAL, TEXT_COLOR), ('4', BTN_COLOR_NORMAL, TEXT_COLOR), ('5', BTN_COLOR_NORMAL, TEXT_COLOR), ('6', BTN_COLOR_NORMAL, TEXT_COLOR), ('-', BTN_COLOR_ACCENT, FG_COLOR),
        # Baris 6
        ('π', BTN_COLOR_NORMAL, TEXT_COLOR), ('1', BTN_COLOR_NORMAL, TEXT_COLOR), ('2', BTN_COLOR_NORMAL, TEXT_COLOR), ('3', BTN_COLOR_NORMAL, TEXT_COLOR), ('+', BTN_COLOR_ACCENT, FG_COLOR),
        # Baris 7
        ('mode', BTN_COLOR_ACCENT, FG_COLOR), ('e', BTN_COLOR_NORMAL, TEXT_COLOR), ('0', BTN_COLOR_NORMAL, TEXT_COLOR), ('.', BTN_COLOR_NORMAL, TEXT_COLOR), ('=', FG_COLOR, BG_COLOR) # '=' memiliki warna khusus
    ]

    cols = 5
    for i, (b_text, b_bg_color, b_fg_color) in enumerate(buttons):
        row_val = i // cols
        col_val = i % cols

        # Penanganan khusus untuk tombol '=' agar lebih besar
        if b_text == '=':
            btn = tk.Button(button_frame, text=b_text, font=("Segoe UI", 20, "bold"), 
                            bg=b_bg_color, fg=b_fg_color, bd=0, 
                            activebackground=ENTRY_BG, activeforeground=b_fg_color,
                            command=lambda val=b_text: click(val))
            btn.grid(row=row_val, column=col_val, rowspan=2, sticky="nsew", padx=3, pady=3) # Mengambil 2 baris
        # Penanganan khusus untuk tombol '0' agar lebih lebar (jika ada) - tidak di gambar, jadi tidak diterapkan
        # elif b_text == '0' and i == len(buttons) - 2: # Misal jika '0' adalah elemen kedua terakhir dan ingin 2 kolom
        #     btn = tk.Button(button_frame, text=b_text, font=("Segoe UI", 18), 
        #                     bg=b_bg_color, fg=b_fg_color, bd=0, activebackground=ENTRY_BG,
        #                     activeforeground=b_fg_color,
        #                     command=lambda val=b_text: click(val))
        #     btn.grid(row=row_val, column=col_val, columnspan=2, sticky="nsew", padx=3, pady=3, ipady=5) # Mengambil 2 kolom
        elif b_text == 'mode': # Placeholder untuk tombol mode, tidak fungsional saat ini
            btn = tk.Button(button_frame, text="🔁", font=("Segoe UI Emoji", 18), 
                            bg=b_bg_color, fg=b_fg_color, bd=0, activebackground=ENTRY_BG,
                            activeforeground=b_fg_color,
                            command=lambda: messagebox.showinfo("Mode", "Fitur mode belum diimplementasikan."))
            btn.grid(row=row_val, column=col_val, sticky="nsew", padx=3, pady=3, ipady=5)
        elif b_text == '2nd': # Placeholder untuk tombol 2nd
             btn = tk.Button(button_frame, text="2nd", font=("Segoe UI", 14), 
                            bg=b_bg_color, fg=b_fg_color, bd=0, activebackground=ENTRY_BG,
                            activeforeground=b_fg_color,
                            command=lambda: messagebox.showinfo("2nd", "Fitur 2nd belum diimplementasikan."))
             btn.grid(row=row_val, column=col_val, sticky="nsew", padx=3, pady=3, ipady=5)
        elif b_text == 'deg': # Placeholder untuk tombol deg/rad
             btn = tk.Button(button_frame, text="deg", font=("Segoe UI", 14), 
                            bg=b_bg_color, fg=b_fg_color, bd=0, activebackground=ENTRY_BG,
                            activeforeground=b_fg_color,
                            command=lambda: messagebox.showinfo("Deg/Rad", "Fitur Deg/Rad belum diimplementasikan."))
             btn.grid(row=row_val, column=col_val, sticky="nsew", padx=3, pady=3, ipady=5)
        else:
            btn = tk.Button(button_frame, text=b_text, font=("Segoe UI", 18), 
                            bg=b_bg_color, fg=b_fg_color, bd=0, activebackground=ENTRY_BG,
                            activeforeground=b_fg_color,
                            command=lambda val=b_text: click(val))
            btn.grid(row=row_val, column=col_val, sticky="nsew", padx=3, pady=3, ipady=5)

    # Konfigurasi grid agar tombol-tombol meluas
    for i in range(cols):
        button_frame.grid_columnconfigure(i, weight=1)
    # Total baris untuk tombol: 7 baris di sini. Perhatikan bahwa '=' mengambil 2 baris terakhir.
    # Jadi kita butuh 7 baris grid
    for i in range(7): # Ada 7 baris tombol (termasuk '=' yang mengambil 2 baris)
        button_frame.grid_rowconfigure(i, weight=1)

# ========================== UNIT CONVERTER CLASS ==============================

class UnitConverterWindow(tk.Toplevel):
    def __init__(self, master, title, unit_data):
        super().__init__(master)
        self.title(title)
        self.configure(bg=BG_COLOR)
        self.geometry("340x550")
        self.resizable(False, False)
        
        self.unit_data = unit_data
        self.expression = tk.StringVar(value="0")
        self.result_var = tk.StringVar(value=f"0 {unit_data['to_unit_name']}")
        
        self._update_conversion()
        
        # --- UI Bagian Atas (Input/Output) ---
        
        # Input (Atas)
        ttk.Label(self, text=f"{self.unit_data['from_unit']} ▾", font=("Segoe UI", 12), 
                  background=BG_COLOR, foreground="#AAAAAA").pack(anchor='w', padx=15, pady=(15, 0))
        
        # Label Input (font dinamis)
        self.input_label = tk.Label(self, textvariable=self.expression, font=("Segoe UI", 24), 
                                    background=BG_COLOR, foreground=FG_COLOR, justify="right", anchor='e', padx=15)
        self.input_label.pack(fill='x', padx=15)
        
        tk.Label(self, text=self.unit_data['from_unit_name'], font=("Segoe UI", 10), 
                 background=BG_COLOR, foreground="#AAAAAA", justify="right", anchor='e').pack(fill='x', padx=15, pady=(0, 10))

        # Divider
        tk.Frame(self, bg=BTN_COLOR_ACCENT, height=2).pack(fill='x', padx=15, pady=5)

        # Output (Bawah)
        ttk.Label(self, text=f"{self.unit_data['to_unit']} ▾", font=("Segoe UI", 12), 
                  background=BG_COLOR, foreground="#AAAAAA").pack(anchor='w', padx=15, pady=(10, 0))
        
        # Label Output (font dinamis)
        self.output_label = tk.Label(self, textvariable=self.result_var, font=("Segoe UI", 24), 
                                     background=BG_COLOR, foreground=TEXT_COLOR, justify="right", anchor='e', padx=15)
        self.output_label.pack(fill='x', padx=15)
        
        tk.Label(self, text=self.unit_data['to_unit_name'], font=("Segoe UI", 10), 
                 background=BG_COLOR, foreground="#AAAAAA", justify="right", anchor='e').pack(fill='x', padx=15, pady=(0, 15))


        # --- Keypad Kalkulator (Mirip Gambar Xiaomi) ---
        
        keypad_frame = tk.Frame(self, bg=BG_COLOR)
        keypad_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        buttons = [
            ('7', BTN_COLOR_NORMAL), ('8', BTN_COLOR_NORMAL), ('9', BTN_COLOR_NORMAL),
            ('4', BTN_COLOR_NORMAL), ('5', BTN_COLOR_NORMAL), ('6', BTN_COLOR_NORMAL),
            ('1', BTN_COLOR_NORMAL), ('2', BTN_COLOR_NORMAL), ('3', BTN_COLOR_NORMAL),
            ('0', BTN_COLOR_NORMAL), ('.', BTN_COLOR_NORMAL), ('', BG_COLOR), 
        ]
        
        side_buttons = [('AC', FG_COLOR), ('Del', FG_COLOR)]

        cols = 4

        def click(key):
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

        # Input untuk angka (3x4)
        for i, (b_text, b_color) in enumerate(buttons):
            row_val = i // 3
            col_val = i % 3
            
            btn = tk.Button(keypad_frame, text=b_text, font=("Segoe UI", 18), 
                            bg=b_color, fg=TEXT_COLOR, bd=0, activebackground=ENTRY_BG,
                            activeforeground=TEXT_COLOR,
                            command=lambda val=b_text: click(val))
            
            if b_text:
                btn.grid(row=row_val, column=col_val, sticky="nsew", padx=3, pady=3, ipady=5)

        # Input untuk AC dan Del (2x1)
        btn_ac = tk.Button(keypad_frame, text=side_buttons[0][0], font=("Segoe UI", 18), 
                        bg=BTN_COLOR_NORMAL, fg=side_buttons[0][1], bd=0, activebackground=ENTRY_BG,
                        activeforeground=side_buttons[0][1],
                        command=lambda val=side_buttons[0][0]: click(val))
        btn_ac.grid(row=0, column=3, rowspan=2, sticky="nsew", padx=3, pady=3)

        btn_del = tk.Button(keypad_frame, text="⌫", font=("Segoe UI", 18), 
                        bg=BTN_COLOR_NORMAL, fg=side_buttons[1][1], bd=0, activebackground=ENTRY_BG,
                        activeforeground=side_buttons[1][1],
                        command=lambda val="Del": click(val))
        btn_del.grid(row=2, column=3, rowspan=2, sticky="nsew", padx=3, pady=3)


        for i in range(cols):
            keypad_frame.grid_columnconfigure(i, weight=1)
        for i in range(4):
            keypad_frame.grid_rowconfigure(i, weight=1)


    def _update_conversion(self):
        try:
            val = float(self.expression.get())
            hasil = self.unit_data['conversion_func'](val)
            formatted_hasil = f"{hasil:.4f}".rstrip('0').rstrip('.')
            self.result_var.set(f"{formatted_hasil} {self.unit_data['to_unit_name']}")
            
            adjust_font_size(self.output_label, self.result_var, max_chars_small=16, max_chars_tiny=22, default_size=24)

        except ValueError:
             self.result_var.set(f"0 {self.unit_data['to_unit_name']}")
        except Exception:
             self.result_var.set("Error")

# ========================== CONVERTER MENU ==============================
class ConverterUI(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Converter Menu")
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