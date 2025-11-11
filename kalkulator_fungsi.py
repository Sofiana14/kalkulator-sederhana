import tkinter as tk
from tkinter import messagebox
import time, math, re
from konstanta import *
from logika_kalkulator import evaluate_expression
from utilitas import adjust_font_size

# ========================== FUNCTION CALCULATOR FRAME ==============================
class FunctionCalculatorFrame(tk.Frame):
    def __init__(self, parent, return_to_menu):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        self.return_to_menu = return_to_menu
        
        self.expression_history = tk.StringVar(value="") 
        self.current_expression = tk.StringVar(value="0") 
        
        # Variabel Mode Kalkulator
        self.is_degree_mode = tk.BooleanVar(value=True) # True = Derajat, False = Radian
        self.is_2nd_mode = tk.BooleanVar(value=False) # False = Fungsi Dasar, True = Fungsi Kedua
        
        # --- Bagian Atas: Tombol Kembali dan Judul ---
        top_controls_frame = tk.Frame(self, bg=BG_COLOR)
        top_controls_frame.pack(fill="x", padx=10, pady=(15, 5))
        
        # Tombol Kembali (Ikon di Kiri Atas)
        back_btn = tk.Button(top_controls_frame, text="←", font=("Segoe UI", 16, "bold"),
                             bg=BG_COLOR, fg=FG_COLOR, bd=0, 
                             activebackground=BTN_COLOR_ACCENT, activeforeground=FG_COLOR,
                             relief=tk.FLAT, 
                             padx=5, pady=5, 
                             command=self.return_to_menu)
        back_btn.pack(side="left") 
        
        # Judul Kalkulator (Pusatkan di sisa ruang)
        title_label = tk.Label(top_controls_frame, text="Kalkulator Fungsi Lanjut", font=("Segoe UI", 14, "bold"), 
                               bg=BG_COLOR, fg=FG_COLOR, anchor="center")
        title_label.pack(side="left", fill="x", expand=True) 
        
        
        # Area tampilan riwayat ekspresi
        self.history_label = tk.Label(self, textvariable=self.expression_history, font=("Segoe UI", 16),
                                     bg=BG_COLOR, fg="#AAAAAA", justify="right", anchor='e',
                                     bd=0, relief=tk.FLAT, padx=10, pady=5)
        self.history_label.pack(padx=10, pady=(5, 0), fill="x")

        # Area tampilan ekspresi utama
        self.entry_label = tk.Label(self, textvariable=self.current_expression, font=("Segoe UI", 32),
                               bg=BG_COLOR, fg=FG_COLOR, justify="right", anchor='e',
                               bd=0, relief=tk.FLAT, padx=10, pady=5)
        self.entry_label.pack(padx=10, pady=(0, 15), fill="x")

        # Label indikator mode sudut (deg/rad)
        self.angle_mode_indicator = tk.Label(self, text="DEG" if self.is_degree_mode.get() else "RAD", 
                                             font=("Segoe UI", 10), bg=BG_COLOR, fg="#AAAAAA", anchor='w', padx=10)
        self.angle_mode_indicator.pack(fill='x', padx=10)

        # Frame untuk tombol kalkulator
        self.button_frame = tk.Frame(self, bg=BG_COLOR)
        self.button_frame.pack(fill="both", padx=5, pady=5) 
        
        # DATA TOMBOL (Menggunakan simbol yang Anda inginkan)
        self.button_data = [
            ('2nd', '2nd', 'mode', 'mode', BTN_COLOR_NORMAL, TEXT_COLOR), ('deg', 'rad', 'deg', 'deg', BTN_COLOR_NORMAL, TEXT_COLOR), 
            ('sin', 'sin⁻¹', 'sin(', 'asin(', BTN_COLOR_NORMAL, TEXT_COLOR), ('cos', 'cos⁻¹', 'cos(', 'acos(', BTN_COLOR_NORMAL, TEXT_COLOR), 
            ('tan', 'tan⁻¹', 'tan(', 'atan(', BTN_COLOR_NORMAL, TEXT_COLOR),
            
            # Tombol pangkat dan logaritma
            ('xʸ', 'yˣ', '^', '^', BTN_COLOR_NORMAL, TEXT_COLOR), 
            ('lg', '10ˣ', 'log(', '10^', BTN_COLOR_NORMAL, TEXT_COLOR), 
            ('ln', 'eˣ', 'ln(', 'e^', BTN_COLOR_NORMAL, TEXT_COLOR), 
            
            ('(', '(', '(', '(', BTN_COLOR_ACCENT, FG_COLOR), 
            (')', ')', ')', ')', BTN_COLOR_ACCENT, FG_COLOR),
            
            # Tombol Akar (Symbolic)
            ('√x', '³√x', 'sqrt(', 'cbrt(', BTN_COLOR_NORMAL, TEXT_COLOR), 
            ('AC', 'AC', 'AC', 'AC', BTN_COLOR_ACCENT, FG_COLOR), 
            ('Del', 'Del', 'Del', 'Del', BTN_COLOR_ACCENT, FG_COLOR), ('%', '%', '%', '%', BTN_COLOR_ACCENT, FG_COLOR), 
            ('/', '/', '/', '/', BTN_COLOR_ACCENT, FG_COLOR),
            
            # Baris 4 (Faktorial)
            ('x!', 'x!', 'x!', 'x!', BTN_COLOR_NORMAL, TEXT_COLOR), ('7', '7', '7', '7', BTN_COLOR_NORMAL, TEXT_COLOR), 
            ('8', '8', '8', '8', BTN_COLOR_NORMAL, TEXT_COLOR), ('9', '9', '9', '9', BTN_COLOR_NORMAL, TEXT_COLOR), 
            ('x', 'x', '*', '*', BTN_COLOR_ACCENT, FG_COLOR),
            
            # Baris 5
            ('1/x', '1/x', '1/', '1/', BTN_COLOR_NORMAL, TEXT_COLOR), ('4', '4', '4', '4', BTN_COLOR_NORMAL, TEXT_COLOR), 
            ('5', '5', '5', '5', BTN_COLOR_NORMAL, TEXT_COLOR), ('6', '6', '6', '6', BTN_COLOR_NORMAL, TEXT_COLOR), 
            ('-', '-', '-', '-', BTN_COLOR_ACCENT, FG_COLOR),
            
            # Baris 6
            ('π', 'π', 'π', 'π', BTN_COLOR_NORMAL, TEXT_COLOR), ('1', '1', '1', '1', BTN_COLOR_NORMAL, TEXT_COLOR), 
            ('2', '2', '2', '2', BTN_COLOR_NORMAL, TEXT_COLOR), ('3', '3', '3', '3', BTN_COLOR_NORMAL, TEXT_COLOR), 
            ('+', '+', '+', '+', BTN_COLOR_ACCENT, FG_COLOR),
            
            # BARIS PALING BAWAH (Row 7)
            ('0', '0', '0', '0', BTN_COLOR_NORMAL, TEXT_COLOR), 
            ('.', '.', '.', '.', BTN_COLOR_NORMAL, TEXT_COLOR), 
            ('00', '00', '00', '00', BTN_COLOR_NORMAL, TEXT_COLOR), 
            ('=', '=', '=', '=', FG_COLOR, BG_COLOR) 
        ]
        self.button_widgets = [] 

        self.create_buttons()
        self.update_button_texts() 


    # --- Fungsi untuk Toggle Mode ---
    def toggle_degree_mode(self):
        self.is_degree_mode.set(not self.is_degree_mode.get())
        self.angle_mode_indicator.config(text="DEG" if self.is_degree_mode.get() else "RAD")

    def toggle_2nd_mode(self):
        self.is_2nd_mode.set(not self.is_2nd_mode.get())
        self.update_button_texts()

    def update_button_texts(self):
        """Memperbarui teks tombol berdasarkan mode 2nd."""
        mode_2nd = self.is_2nd_mode.get()
        for i, btn_widget in enumerate(self.button_widgets):
            if i >= len(self.button_data):
                continue

            text_normal, text_2nd, click_normal, click_2nd, b_bg_color, b_fg_color = self.button_data[i]
            
            new_text = text_2nd if mode_2nd else text_normal
            click_value = click_2nd if mode_2nd else click_normal
            
            # Tombol 2nd/deg
            if text_normal == '2nd':
                new_text = "2nd"
                click_value = 'mode'
            elif text_normal == 'deg':
                new_text = "RAD" if self.is_degree_mode.get() else "DEG"
                click_value = 'deg'
            
            btn_widget.config(text=new_text, command=lambda val=click_value: self.click(val))
            
            # Warna 2nd
            if text_normal == '2nd' and mode_2nd:
                btn_widget.config(bg=FG_COLOR, fg=BG_COLOR, activebackground=ENTRY_BG, activeforeground=BG_COLOR)
            elif text_normal == '2nd':
                btn_widget.config(bg=BTN_COLOR_NORMAL, fg=TEXT_COLOR, activebackground=ENTRY_BG, activeforeground=TEXT_COLOR)
            
            # --- FONT UNTUK SIMBOL DI SINI ---
            is_special_symbol = new_text in ('sin⁻¹', 'cos⁻¹', 'tan⁻¹', '√x', '³√x')
            
            if is_special_symbol:
                # Ganti ke font yang lebih kompatibel dengan Unicode
                font_family = "Arial Unicode MS" 
                font_size = 18 
                font_weight = "normal"
                btn_widget.config(font=(font_family, font_size, font_weight))
            elif text_normal == '=':
                 btn_widget.config(font=("Segoe UI", 20, "normal"))
            else:
                # Reset font untuk tombol numerik/standar lainnya
                font_size = 18
                if text_normal in ('2nd', 'deg'): font_size = 14
                if text_normal in ('xʸ', 'yˣ', '10ˣ', 'eˣ', 'x!'): font_weight = "normal"
                else: font_weight = "normal"
                btn_widget.config(font=("Segoe UI", font_size, font_weight))


    # --- Click Handler untuk Kalkulator Fungsi ---
    def click(self, key):
        """Logika penanganan klik tombol kalkulator fungsi."""
        hist = self.expression_history.get()
        curr = self.current_expression.get()

        if key == "mode":
            self.toggle_2nd_mode()
            return
        elif key == "deg":
            self.toggle_degree_mode()
            return
        
        if key == "AC":
            self.current_expression.set("0")
            self.expression_history.set("")
        elif key == "Del":
            if curr == "0" or "Error" in curr or "Invalid Input" in curr or "Domain Error" in curr or "Div/0 Error" in curr:
                self.current_expression.set("0")
            elif len(curr) > 1:
                self.current_expression.set(curr[:-1])
            else:
                self.current_expression.set("0")
        elif key == "=":
            try:
                # Logika Evaluasi
                display_expr = curr.replace('^', '**').replace('x', '*')
                display_expr = display_expr.replace('π', str(math.pi)).replace('e', str(math.e))
                
                # Mengganti fungsi standar dengan fungsi math
                display_expr = re.sub(r'log(\()', r'math.log10\1', display_expr) 
                display_expr = re.sub(r'ln(\()', r'math.log\1', display_expr) 
                display_expr = re.sub(r'sqrt(\()', r'math.sqrt\1', display_expr)
                
                # Penggantian cbrt(x) menjadi math.pow(x, 1/3)
                if 'cbrt(' in display_expr:
                    def replace_cbrt(match):
                        arg = match.group(1) 
                        return f'math.pow({arg}, 1/3)'

                    pattern_cbrt = r'cbrt\(([^)]+)\)' 
                    display_expr = re.sub(pattern_cbrt, replace_cbrt, display_expr)


                trig_funcs = {'sin': 'math.sin', 'cos': 'math.cos', 'tan': 'math.tan', 
                              'asin': 'math.asin', 'acos': 'math.acos', 'atan': 'math.atan'}

                processed_expr = display_expr
                for func_name, math_func in trig_funcs.items():
                    if func_name in processed_expr:
                        pattern = r'({}\()([^)]+)(\))'.format(re.escape(func_name))
                        
                        def replace_trig(match):
                            arg = match.group(2)
                            if func_name in ['sin', 'cos', 'tan'] and self.is_degree_mode.get():
                                return f'{math_func}(math.radians({arg}))'
                            else:
                                return f'{math_func}({arg})'

                        processed_expr = re.sub(pattern, replace_trig, processed_expr)

                final_expr = processed_expr
                
                if '!' in final_expr:
                    final_expr = re.sub(r'(\d+)!', r'math.factorial(\1)', final_expr)

                result = evaluate_expression(final_expr)
                
                if isinstance(result, str):
                    self.current_expression.set(result) 
                    self.expression_history.set("")
                    return
                
                self.expression_history.set(curr + "=")
                
                if isinstance(result, (int, float)):
                    result = round(result, 10) 
                
                self.current_expression.set(str(result))
            except Exception as e:
                self.current_expression.set("Error")
                self.expression_history.set("")
        else:
            if curr == "0" or "Error" in curr or "Invalid Input" in curr or "Domain Error" in curr or "Div/0 Error" in curr:
                if key in ('+', '-', '*', '/', '^', '%', 'x!'):
                    self.current_expression.set(curr + key)
                elif key.endswith('(') or key in ('π', 'e', '10^', 'e^'):
                    self.current_expression.set(key) 
                else:
                    self.current_expression.set(key)
            else:
                self.current_expression.set(curr + key)
        
        adjust_font_size(self.entry_label, self.current_expression, max_chars_small=12, max_chars_tiny=18, default_size=32)

    def create_buttons(self):
        """Membuat dan menempatkan semua tombol kalkulator fungsi."""
        cols = 5
        
        current_col = 0
        current_row = 0
        
        INDEX_OF_ZERO = 30
        
        for i, (text_normal, text_2nd, click_normal, click_2nd, b_bg_color, b_fg_color) in enumerate(self.button_data):
            b_text = text_normal
            click_value = click_normal
            
            # Logika Tata Letak
            colspan = 1
            if i > 0 and i % cols == 0 and i != INDEX_OF_ZERO:
                current_col = 0
                current_row += 1
            
            if i == INDEX_OF_ZERO: 
                colspan = 2 
                current_col = 0
                current_row = 6 
            
            elif i > INDEX_OF_ZERO:
                current_col = 2 + (i - (INDEX_OF_ZERO + 1)) 

            # Tentukan font
            font_size = 18 
            font_weight = "normal"
            font_family = "Segoe UI"
            
            if b_text in ('2nd', 'deg', 'RAD', 'DEG'):
                font_size = 14
            elif b_text == '=':
                font_size = 20
                font_weight = "bold"
            elif b_text in ('xʸ', 'yˣ', '10ˣ', 'eˣ', 'x!'):
                font_size = 18
                font_weight = "bold"
            
            # FONT KHUSUS UNTUK SIMBOL
            elif b_text in ('sin⁻¹', 'cos⁻¹', 'tan⁻¹', '√x', '³√x'):
                font_family = "Arial Unicode MS" # Ganti font di sini!
                font_size = 18 

            if current_row == 6 and b_text not in ('='):
                 font_size = 18

            font = (font_family, font_size, font_weight)

            btn = tk.Button(self.button_frame, text=b_text, font=font, 
                             bg=b_bg_color, fg=b_fg_color, bd=0, activebackground=ENTRY_BG,
                             activeforeground=b_fg_color,
                             command=lambda val=click_value: self.click(val))
            
            if i < INDEX_OF_ZERO:
                 row_to_use = i // cols
                 col_to_use = i % cols
                 btn.grid(row=row_to_use, column=col_to_use, sticky="nsew", padx=3, pady=3, ipady=5, columnspan=colspan)
            else:
                 btn.grid(row=current_row, column=current_col, sticky="nsew", padx=3, pady=3, ipady=5, columnspan=colspan)


            self.button_widgets.append(btn)
            
            if i < INDEX_OF_ZERO and i % cols != cols - 1:
                current_col = (i % cols) + 1
            elif i < INDEX_OF_ZERO and i % cols == cols - 1:
                current_col = cols

        # Konfigurasi grid agar tombol dapat diregangkan
        for i in range(cols):
            self.button_frame.grid_columnconfigure(i, weight=1)
        for i in range(7): 
            self.button_frame.grid_rowconfigure(i, weight=1)