import tkinter as tk
from konstanta import *
from logika_kalkulator import evaluate_expression
from utilitas import adjust_font_size
import re

# ========================== BASIC CALCULATOR FRAME ==============================
class BasicCalculatorFrame(tk.Frame):
    def __init__(self, parent, return_to_menu):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        
        self.return_to_menu = return_to_menu
        
        self.expression = tk.StringVar(value="0")

        # --- Bagian Atas: Tombol Kembali dan Judul ---
        top_controls_frame = tk.Frame(self, bg=BG_COLOR)
        top_controls_frame.pack(fill="x", padx=10, pady=(15, 5))
        
        # Tombol Kembali (Mencocokkan ukuran dan font FunctionFrame)
        back_btn = tk.Button(top_controls_frame, text="←", font=("Segoe UI", 16, "bold"),
                             bg=BG_COLOR, fg=FG_COLOR, bd=0, 
                             activebackground=BTN_COLOR_ACCENT, activeforeground=FG_COLOR,
                             relief=tk.FLAT, 
                             padx=5, pady=5, 
                             command=self.return_to_menu)
        back_btn.pack(side="left") 
        
        # Judul Kalkulator
        title_label = tk.Label(top_controls_frame, text="Kalkulator Dasar", font=("Segoe UI", 14, "bold"), 
                               bg=BG_COLOR, fg=FG_COLOR, anchor="center")
        title_label.pack(side="left", fill="x", expand=True) 
        
        # Display Entry (Mencocokkan gaya FunctionFrame, namun ukuran font disesuaikan agar tidak terlalu besar)
        self.entry = tk.Label(self, textvariable=self.expression, font=("Segoe UI", 32), # Font size lebih besar
                           bg=BG_COLOR, fg=FG_COLOR, justify="right", anchor='e', # Ganti ENTRY_BG ke BG_COLOR dan TEXT_COLOR ke FG_COLOR
                           bd=0, relief=tk.FLAT, padx=10)
        self.entry.pack(padx=10, pady=(10, 15), fill="x", ipady=10) # Padding sedikit diubah
        
        # --- Bagian Tengah: Tombol Kalkulator ---
        self.button_frame = tk.Frame(self, bg=BG_COLOR)
        self.button_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        self.create_buttons()


    def click(self, key):
        """Logika penanganan klik tombol."""
        current_expression = self.expression.get()
        
        if "Error" in current_expression or "Invalid Input" in current_expression or "Div/0" in current_expression:
            if key in ('AC', 'Del', '='):
                self.expression.set("0")
                # Gunakan parameter font size FunctionCalculatorFrame
                adjust_font_size(self.entry, self.expression, max_chars_small=12, max_chars_tiny=18, default_size=32)
                return
            else:
                 current_expression = "0"
        
        # Ganti simbol √ dan log dengan sintaks yang benar sebelum dievaluasi
        if key == '√': 
             key = 'sqrt('
        elif key == 'log':
             key = 'log(' 

        if key == "=":
            result = evaluate_expression(current_expression)
            
            if isinstance(result, str) and ("Error" in result or "Div/0" in result or "Syntax" in result or "Domain" in result):
                self.expression.set(result)
            else:
                self.expression.set(str(result))
                
        elif key == "AC":
            self.expression.set("0")
        elif key == "Del":
            if len(current_expression) > 1 and current_expression != "0":
                self.expression.set(current_expression[:-1])
            else:
                self.expression.set("0")
        elif key == '%':
            try:
                if "Error" not in current_expression:
                    result = evaluate_expression(current_expression.replace('%', '/100'))
                    self.expression.set(str(result))
                else:
                    self.expression.set("Error")
            except Exception:
                self.expression.set("Error")
        elif key.endswith('('): # Untuk sqrt( dan log(
            if current_expression == "0" or "Error" in current_expression:
                self.expression.set(key)
            else:
                self.expression.set(current_expression + key)
        else:
            if current_expression == "0":
                current_expression = ""
            self.expression.set(current_expression + key)
        
        # Gunakan parameter font size FunctionCalculatorFrame
        adjust_font_size(self.entry, self.expression, max_chars_small=12, max_chars_tiny=18, default_size=32)


    def create_buttons(self):
        """Membuat dan menempatkan semua tombol kalkulator."""
        # Tombol Datar (5x5)
        buttons = [
            ('AC', BTN_COLOR_ACCENT), ('Del', BTN_COLOR_ACCENT), ('(', BTN_COLOR_ACCENT), (')', BTN_COLOR_ACCENT), ('/', BTN_COLOR_ACCENT),
            ('7', BTN_COLOR_NORMAL), ('8', BTN_COLOR_NORMAL), ('9', BTN_COLOR_NORMAL), ('*', BTN_COLOR_ACCENT), ('%', BTN_COLOR_ACCENT),
            ('4', BTN_COLOR_NORMAL), ('5', BTN_COLOR_NORMAL), ('6', BTN_COLOR_NORMAL), ('-', BTN_COLOR_ACCENT), ('√', BTN_COLOR_ACCENT), 
            ('1', BTN_COLOR_NORMAL), ('2', BTN_COLOR_NORMAL), ('3', BTN_COLOR_NORMAL), ('+', BTN_COLOR_ACCENT), ('=', BG_COLOR),
            ('0', BTN_COLOR_NORMAL), ('.', BTN_COLOR_NORMAL), ('00', BTN_COLOR_NORMAL), ('^', BTN_COLOR_ACCENT), ('log', BTN_COLOR_ACCENT)
        ]

        cols = 5
        for i, (b_text, b_color) in enumerate(buttons):
            row_val = i // cols
            col_val = i % cols
            
            # --- Tentukan FONT (Mencocokkan FunctionCalculatorFrame) ---
            font_size = 18 
            font_family = "Segoe UI"
            font_weight = "normal"
            
            if b_text in ('√', 'log', '^'):
                font_family = "Arial Unicode MS" # Font untuk simbol
                font_size = 18 
            elif b_text == '=':
                font_size = 20
                font_weight = "bold"
            
            btn_font = (font_family, font_size, font_weight)
            # --- End FONT ---


            if b_text == '=':
                btn_bg = FG_COLOR 
                btn_fg = BG_COLOR
                active_fg = BG_COLOR
            elif b_color == BTN_COLOR_ACCENT:
                btn_bg = BTN_COLOR_ACCENT
                btn_fg = FG_COLOR
                active_fg = FG_COLOR
            else:
                btn_bg = BTN_COLOR_NORMAL
                btn_fg = TEXT_COLOR
                active_fg = TEXT_COLOR
            
            # PADDING PADA TOMBOL (Mencocokkan FunctionCalculatorFrame)
            btn = tk.Button(self.button_frame, text=b_text, font=btn_font, 
                             bg=btn_bg, fg=btn_fg, bd=0, activebackground=ENTRY_BG,
                             activeforeground=active_fg,
                             command=lambda val=b_text: self.click(val))
            
            # PADDING GRID (Mencocokkan FunctionCalculatorFrame)
            btn.grid(row=row_val, column=col_val, sticky="nsew", padx=3, pady=3, ipady=5)

        # Konfigurasi grid agar tombol dapat diregangkan
        for i in range(cols):
            self.button_frame.grid_columnconfigure(i, weight=1)
        for i in range(5): 
            self.button_frame.grid_rowconfigure(i, weight=1)