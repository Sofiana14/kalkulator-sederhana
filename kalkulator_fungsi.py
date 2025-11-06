import tkinter as tk
from tkinter import messagebox
import time, math, re
from konstanta import *
from logika_kalkulator import evaluate_expression
from utilitas import adjust_font_size # Import dari utilitas.py

# ========================== FUNCTION CALCULATOR ==============================
def open_function_calculator(root):
    win = tk.Toplevel(root)
    win.title("Kalkulator Fungsi Lanjut")
    win.geometry("380x600") 
    win.configure(bg=BG_COLOR)
    win.resizable(True, True) 

    expression_history = tk.StringVar(value="") 
    current_expression = tk.StringVar(value="0") 
    
    # Area tampilan riwayat ekspresi
    history_label = tk.Label(win, textvariable=expression_history, font=("Segoe UI", 16),
                             bg=BG_COLOR, fg="#AAAAAA", justify="right", anchor='e',
                             bd=0, relief=tk.FLAT, padx=10, pady=5)
    history_label.pack(padx=10, pady=(15, 0), fill="x")

    # Area tampilan ekspresi utama
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
                # Logika evaluasi 
                display_expr = curr.replace('^', '**').replace('x', '*')
                display_expr = display_expr.replace('π', str(math.pi)).replace('e', str(math.e))
                
                display_expr = re.sub(r'log(\()', r'math.log10\1', display_expr) 
                display_expr = re.sub(r'ln(\()', r'math.log\1', display_expr) 
                display_expr = re.sub(r'sqrt(\()', r'math.sqrt\1', display_expr)
                display_expr = re.sub(r'sin(\()', r'math.sin(math.radians(', display_expr)
                display_expr = re.sub(r'cos(\()', r'math.cos(math.radians(', display_expr)
                display_expr = re.sub(r'tan(\()', r'math.tan(math.radians(', display_expr)
                
                if 'math.radians(' in display_expr: 
                    display_expr += '))'

                result = evaluate_expression(display_expr)
                expression_history.set(curr + "=")
                current_expression.set(str(result))
            except Exception as e:
                current_expression.set("Error")
                expression_history.set("")
        else:
            if curr == "0" or curr == "Error" or curr == "Invalid Input":
                # Logika penanganan input awal
                if key in ('+', '-', '*', '/', '^', '%', 'x!'):
                    current_expression.set(curr + key)
                elif key in ('sin(', 'cos(', 'tan(', 'log(', 'sqrt(', 'ln(', 'lg(', 'π', 'e'):
                    current_expression.set(key) 
                else:
                    current_expression.set(key)
            else:
                current_expression.set(curr + key)
        
        adjust_font_size(entry_label, current_expression, max_chars_small=12, max_chars_tiny=18, default_size=32)

    # --- Frame untuk tombol kalkulator ---
    button_frame = tk.Frame(win, bg=BG_COLOR)
    button_frame.pack(expand=True, fill="both", padx=5, pady=5)
    
    # Tombol-tombol untuk kalkulator fungsi
    buttons = [
        ('2nd', BTN_COLOR_NORMAL, TEXT_COLOR), ('deg', BTN_COLOR_NORMAL, TEXT_COLOR), ('sin', BTN_COLOR_NORMAL, TEXT_COLOR), ('cos', BTN_COLOR_NORMAL, TEXT_COLOR), ('tan', BTN_COLOR_NORMAL, TEXT_COLOR),
        ('x^y', BTN_COLOR_NORMAL, TEXT_COLOR), ('lg', BTN_COLOR_NORMAL, TEXT_COLOR), ('ln', BTN_COLOR_NORMAL, TEXT_COLOR), ('(', BTN_COLOR_ACCENT, FG_COLOR), (')', BTN_COLOR_ACCENT, FG_COLOR),
        ('sqrt', BTN_COLOR_NORMAL, TEXT_COLOR), ('AC', BTN_COLOR_ACCENT, FG_COLOR), ('Del', BTN_COLOR_ACCENT, FG_COLOR), ('%', BTN_COLOR_ACCENT, FG_COLOR), ('/', BTN_COLOR_ACCENT, FG_COLOR),
        ('x!', BTN_COLOR_NORMAL, TEXT_COLOR), ('7', BTN_COLOR_NORMAL, TEXT_COLOR), ('8', BTN_COLOR_NORMAL, TEXT_COLOR), ('9', BTN_COLOR_NORMAL, TEXT_COLOR), ('x', BTN_COLOR_ACCENT, FG_COLOR),
        ('1/x', BTN_COLOR_NORMAL, TEXT_COLOR), ('4', BTN_COLOR_NORMAL, TEXT_COLOR), ('5', BTN_COLOR_NORMAL, TEXT_COLOR), ('6', BTN_COLOR_NORMAL, TEXT_COLOR), ('-', BTN_COLOR_ACCENT, FG_COLOR),
        ('π', BTN_COLOR_NORMAL, TEXT_COLOR), ('1', BTN_COLOR_NORMAL, TEXT_COLOR), ('2', BTN_COLOR_NORMAL, TEXT_COLOR), ('3', BTN_COLOR_NORMAL, TEXT_COLOR), ('+', BTN_COLOR_ACCENT, FG_COLOR),
        ('mode', BTN_COLOR_ACCENT, FG_COLOR), ('e', BTN_COLOR_NORMAL, TEXT_COLOR), ('0', BTN_COLOR_NORMAL, TEXT_COLOR), ('.', BTN_COLOR_NORMAL, TEXT_COLOR), ('=', FG_COLOR, BG_COLOR)
    ]

    cols = 5
    for i, (b_text, b_bg_color, b_fg_color) in enumerate(buttons):
        row_val = i // cols
        col_val = i % cols

        if b_text == '=':
            btn = tk.Button(button_frame, text=b_text, font=("Segoe UI", 20, "bold"), 
                            bg=b_bg_color, fg=b_fg_color, bd=0, 
                            activebackground=ENTRY_BG, activeforeground=b_fg_color,
                            command=lambda val=b_text: click(val))
            btn.grid(row=row_val, column=col_val, rowspan=2, sticky="nsew", padx=3, pady=3) 
        elif b_text in ('mode', '2nd', 'deg'): 
            display_text = "🔁" if b_text == 'mode' else b_text
            font_size = ("Segoe UI Emoji", 18) if b_text == 'mode' else ("Segoe UI", 14)
            btn = tk.Button(button_frame, text=display_text, font=font_size, 
                            bg=b_bg_color, fg=b_fg_color, bd=0, activebackground=ENTRY_BG,
                            activeforeground=b_fg_color,
                            command=lambda t=b_text: messagebox.showinfo(t.capitalize(), f"Fitur {t} belum diimplementasikan."))
            btn.grid(row=row_val, column=col_val, sticky="nsew", padx=3, pady=3, ipady=5)
        else:
            btn = tk.Button(button_frame, text=b_text, font=("Segoe UI", 18), 
                            bg=b_bg_color, fg=b_fg_color, bd=0, activebackground=ENTRY_BG,
                            activeforeground=b_fg_color,
                            command=lambda val=b_text: click(val))
            btn.grid(row=row_val, column=col_val, sticky="nsew", padx=3, pady=3, ipady=5)

    for i in range(cols):
        button_frame.grid_columnconfigure(i, weight=1)
    for i in range(7): 
        button_frame.grid_rowconfigure(i, weight=1)