# kalkulator_dasar.py

import tkinter as tk
from konstanta import *
from logika_kalkulator import evaluate_expression
from utilitas import adjust_font_size

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
            
            # CEK HASIL: Jika berupa string error spesifik, tampilkan
            if isinstance(result, str) and ("Error" in result or "Div/0" in result or "Syntax" in result or "Domain" in result):
                expression.set(result)
            else:
                # Hasil valid
                expression.set(str(result))
                
        elif key == "AC":
            expression.set("0")
        elif key == "Del":
            if len(current_expression) > 1 and "Error" not in current_expression:
                expression.set(current_expression[:-1])
            else:
                expression.set("0")
        elif key in ('sqrt', 'log'): 
            if current_expression == "0" or "Error" in current_expression:
                expression.set(key + '(')
            else:
                expression.set(current_expression + key + '(')
        elif key == '%':
            try:
                # Hanya ganti % jika input bukan Error
                if "Error" not in current_expression:
                    result = evaluate_expression(current_expression.replace('%', '/100'))
                    expression.set(str(result))
                else:
                    expression.set("Error")
            except Exception:
                expression.set("Error")
        else:
            if current_expression == "0" or "Error" in current_expression:
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