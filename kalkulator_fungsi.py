import tkinter as tk
from tkinter import messagebox
import time, math, re
from konstanta import *
from logika_kalkulator import evaluate_expression
from utilitas import adjust_font_size

# ========================== FUNCTION CALCULATOR ==============================
def open_function_calculator(root):
    win = tk.Toplevel(root)
    win.title("Kalkulator Fungsi Lanjut")
    win.geometry("380x600") 
    win.configure(bg=BG_COLOR)
    win.resizable(True, True) 

    expression_history = tk.StringVar(value="") 
    current_expression = tk.StringVar(value="0") 
    
    # --- Variabel Mode Kalkulator Baru ---
    # Mode Satuan Sudut: True = Derajat, False = Radian (Default: Derajat agar sesuai dengan implementasi sebelumnya)
    is_degree_mode = tk.BooleanVar(value=True) 
    # Mode Fungsi: False = Fungsi Dasar (sin, cos, ...), True = Fungsi Kedua (asin, acos, ...)
    is_2nd_mode = tk.BooleanVar(value=False) 
    
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

    # Label indikator mode sudut (deg/rad)
    angle_mode_indicator = tk.Label(win, textvariable="DEG" if is_degree_mode.get() else "RAD", 
                                    font=("Segoe UI", 10), bg=BG_COLOR, fg="#AAAAAA", anchor='w', padx=10)
    angle_mode_indicator.pack(fill='x', padx=10)


    # --- Fungsi untuk Toggle Mode ---
    def toggle_degree_mode():
        is_degree_mode.set(not is_degree_mode.get())
        angle_mode_indicator.config(text="DEG" if is_degree_mode.get() else "RAD")

    def toggle_2nd_mode():
        is_2nd_mode.set(not is_2nd_mode.get())
        # Memanggil update_button_texts untuk memperbarui tampilan
        update_button_texts() 

    # --- Click Handler untuk Kalkulator Fungsi ---
    def click(key):
        hist = expression_history.get()
        curr = current_expression.get()

        # Tombol Khusus Mode
        if key == "mode":
            toggle_2nd_mode()
            return
        elif key == "deg":
            toggle_degree_mode()
            return
        
        # ... (Logika AC, Del, dan input lainnya tetap)
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
                # Logika evaluasi (Disesuaikan untuk mode sudut)
                display_expr = curr.replace('^', '**').replace('x', '*')
                display_expr = display_expr.replace('π', str(math.pi)).replace('e', str(math.e))
                
                # Mengganti fungsi standar dengan fungsi math
                display_expr = re.sub(r'log(\()', r'math.log10\1', display_expr) 
                display_expr = re.sub(r'ln(\()', r'math.log\1', display_expr) 
                display_expr = re.sub(r'sqrt(\()', r'math.sqrt\1', display_expr)
                
                # Penanganan fungsi trigonometri (sin, cos, tan, asin, acos, atan)
                trig_funcs = {'sin': 'math.sin', 'cos': 'math.cos', 'tan': 'math.tan', 
                              'asin': 'math.asin', 'acos': 'math.acos', 'atan': 'math.atan'}

                for func_name, math_func in trig_funcs.items():
                    # Menambahkan logika konversi ke radian jika mode Derajat aktif
                    if func_name in display_expr:
                        if func_name in ['sin', 'cos', 'tan'] and is_degree_mode.get():
                            # Konversi input sudut ke radian
                            display_expr = re.sub(r'{}\('.format(func_name), r'{}(math.radians('.format(math_func), display_expr)
                            display_expr += ')' # Tambahkan tutup kurung untuk math.radians
                        elif func_name in ['asin', 'acos', 'atan'] and is_degree_mode.get():
                            # Hasil fungsi invers (misalnya asin) adalah radian, konversi ke derajat

                            # Fungsi invers (asin/acos/atan) akan mengembalikan radian, yang dianggap sebagai nilai numerik murni.
                            display_expr = re.sub(r'{}\('.format(func_name), r'{}\('.format(math_func), display_expr) 
                        else:
                            # Jika mode radian, gunakan fungsi math murni
                            display_expr = re.sub(r'{}\('.format(func_name), r'{}\('.format(math_func), display_expr)


                result = evaluate_expression(display_expr)
                expression_history.set(curr + "=")
                
                # Pembulatan yang lebih baik
                if isinstance(result, (int, float)):
                    result = round(result, 10) 
                
                current_expression.set(str(result))
            except Exception as e:
                current_expression.set("Error")
                expression_history.set("")
        else:
            # ... (Logika input lainnya tetap)
            if curr == "0" or curr == "Error" or curr == "Invalid Input":
                if key in ('+', '-', '*', '/', '^', '%', 'x!'):
                    current_expression.set(curr + key)
                elif key in ('sin(', 'cos(', 'tan(', 'log(', 'sqrt(', 'ln(', 'lg(', 'π', 'e', 'asin(', 'acos(', 'atan('):
                    current_expression.set(key) 
                else:
                    current_expression.set(key)
            else:
                current_expression.set(curr + key)
        
        adjust_font_size(entry_label, current_expression, max_chars_small=12, max_chars_tiny=18, default_size=32)

    # --- Frame untuk tombol kalkulator ---
    button_frame = tk.Frame(win, bg=BG_COLOR)
    button_frame.pack(expand=True, fill="both", padx=5, pady=5)
    
    # Daftar tombol awal dan 2nd
    button_data = [
        # (text_normal, text_2nd, click_value_normal, click_value_2nd, bg_color, fg_color)
        ('2nd', '2nd', 'mode', 'mode', BTN_COLOR_NORMAL, TEXT_COLOR), ('deg', 'rad', 'deg', 'deg', BTN_COLOR_NORMAL, TEXT_COLOR), 
        ('sin', 'asin', 'sin(', 'asin(', BTN_COLOR_NORMAL, TEXT_COLOR), ('cos', 'acos', 'cos(', 'acos(', BTN_COLOR_NORMAL, TEXT_COLOR), 
        ('tan', 'atan', 'tan(', 'atan(', BTN_COLOR_NORMAL, TEXT_COLOR),
        
        ('x^y', 'y^x', '^', '^', BTN_COLOR_NORMAL, TEXT_COLOR), ('lg', '10^x', 'log(', '10^', BTN_COLOR_NORMAL, TEXT_COLOR), 
        ('ln', 'e^x', 'ln(', 'e^', BTN_COLOR_NORMAL, TEXT_COLOR), ('(', '(', '(', '(', BTN_COLOR_ACCENT, FG_COLOR), 
        (')', ')', ')', ')', BTN_COLOR_ACCENT, FG_COLOR),
        
        ('sqrt', 'cbrt', 'sqrt(', 'cbrt', BTN_COLOR_NORMAL, TEXT_COLOR), ('AC', 'AC', 'AC', 'AC', BTN_COLOR_ACCENT, FG_COLOR), 
        ('Del', 'Del', 'Del', 'Del', BTN_COLOR_ACCENT, FG_COLOR), ('%', '%', '%', '%', BTN_COLOR_ACCENT, FG_COLOR), 
        ('/', '/', '/', '/', BTN_COLOR_ACCENT, FG_COLOR),
        
        ('x!', 'x!', 'x!', 'x!', BTN_COLOR_NORMAL, TEXT_COLOR), ('7', '7', '7', '7', BTN_COLOR_NORMAL, TEXT_COLOR), 
        ('8', '8', '8', '8', BTN_COLOR_NORMAL, TEXT_COLOR), ('9', '9', '9', '9', BTN_COLOR_NORMAL, TEXT_COLOR), 
        ('x', 'x', '*', '*', BTN_COLOR_ACCENT, FG_COLOR),
        
        ('1/x', '1/x', '1/', '1/', BTN_COLOR_NORMAL, TEXT_COLOR), ('4', '4', '4', '4', BTN_COLOR_NORMAL, TEXT_COLOR), 
        ('5', '5', '5', '5', BTN_COLOR_NORMAL, TEXT_COLOR), ('6', '6', '6', '6', BTN_COLOR_NORMAL, TEXT_COLOR), 
        ('-', '-', '-', '-', BTN_COLOR_ACCENT, FG_COLOR),
        
        ('π', 'π', 'π', 'π', BTN_COLOR_NORMAL, TEXT_COLOR), ('1', '1', '1', '1', BTN_COLOR_NORMAL, TEXT_COLOR), 
        ('2', '2', '2', '2', BTN_COLOR_NORMAL, TEXT_COLOR), ('3', '3', '3', '3', BTN_COLOR_NORMAL, TEXT_COLOR), 
        ('+', '+', '+', '+', BTN_COLOR_ACCENT, FG_COLOR),
        
        ('mode', 'e', 'mode', 'e', BTN_COLOR_ACCENT, FG_COLOR), ('e', 'e', 'e', 'e', BTN_COLOR_NORMAL, TEXT_COLOR), 
        ('0', '0', '0', '0', BTN_COLOR_NORMAL, TEXT_COLOR), ('.', '.', '.', '.', BTN_COLOR_NORMAL, TEXT_COLOR), 
        ('=', '=', '=', '=', FG_COLOR, BG_COLOR)
    ]
    
    button_widgets = [] # Daftar untuk menyimpan widget tombol

    # Fungsi untuk memperbarui teks tombol berdasarkan mode 2nd
    def update_button_texts():
        mode_2nd = is_2nd_mode.get()
        for i, btn_widget in enumerate(button_widgets):
            text_normal, text_2nd, click_normal, click_2nd, b_bg_color, b_fg_color = button_data[i]
            
            new_text = text_2nd if mode_2nd else text_normal
            click_value = click_2nd if mode_2nd else click_normal
            
            # Khusus untuk tombol mode/2nd/deg
            if text_normal == 'mode':
                new_text = "🔁" 
                click_value = 'mode'
            elif text_normal == '2nd':
                new_text = "2nd"
                click_value = 'mode'
            elif text_normal == 'deg':
                new_text = "RAD" if mode_2nd else "DEG"
                click_value = 'deg'
                
            btn_widget.config(text=new_text, command=lambda val=click_value: click(val))
            
            # Ganti warna tombol 2nd/mode/deg jika mode aktif
            if (text_normal == '2nd' and mode_2nd) or (text_normal == 'deg' and mode_2nd):
                btn_widget.config(bg=FG_COLOR, fg=BG_COLOR, activebackground=ENTRY_BG, activeforeground=BG_COLOR)
            elif text_normal == '2nd' or text_normal == 'deg':
                btn_widget.config(bg=BTN_COLOR_NORMAL, fg=TEXT_COLOR, activebackground=ENTRY_BG, activeforeground=TEXT_COLOR)

    # Pembuatan tombol
    cols = 5
    for i, (text_normal, text_2nd, click_normal, click_2nd, b_bg_color, b_fg_color) in enumerate(button_data):
        row_val = i // cols
        col_val = i % cols
        
        # Penentuan teks dan nilai klik awal (mode normal)
        b_text = text_normal
        click_value = click_normal
        
        if b_text == 'mode':
            b_text = "🔁"
        elif b_text == '2nd':
            b_text = "2nd"

        if b_text == '=':
            btn = tk.Button(button_frame, text=b_text, font=("Segoe UI", 20, "bold"), 
                            bg=b_bg_color, fg=b_fg_color, bd=0, 
                            activebackground=ENTRY_BG, activeforeground=b_fg_color,
                            command=lambda val=click_value: click(val))
            btn.grid(row=row_val, column=col_val, rowspan=2, sticky="nsew", padx=3, pady=3) 
        elif b_text in ('2nd', 'deg', '🔁'): 
            font_size = ("Segoe UI Emoji", 18) if b_text == '🔁' else ("Segoe UI", 14)
            btn = tk.Button(button_frame, text=b_text, font=font_size, 
                            bg=b_bg_color, fg=b_fg_color, bd=0, activebackground=ENTRY_BG,
                            activeforeground=b_fg_color,
                            command=lambda val=click_value: click(val))
            btn.grid(row=row_val, column=col_val, sticky="nsew", padx=3, pady=3, ipady=5)
        else:
            btn = tk.Button(button_frame, text=b_text, font=("Segoe UI", 18), 
                            bg=b_bg_color, fg=b_fg_color, bd=0, activebackground=ENTRY_BG,
                            activeforeground=b_fg_color,
                            command=lambda val=click_value: click(val))
            btn.grid(row=row_val, column=col_val, sticky="nsew", padx=3, pady=3, ipady=5)
            
        button_widgets.append(btn)


    for i in range(cols):
        button_frame.grid_columnconfigure(i, weight=1)
    for i in range(7): 
        button_frame.grid_rowconfigure(i, weight=1)
        
    # Panggil fungsi update untuk memastikan inisialisasi yang benar
    update_button_texts()