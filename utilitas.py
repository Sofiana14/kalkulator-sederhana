# utilitas.py

import tkinter as tk
import re 

# ========================== FUNGSI UTILITAS FONT DINAMIS ==========================
def adjust_font_size(widget, text_var, max_chars_small, max_chars_tiny, default_size):
    """Menyesuaikan ukuran font pada widget berdasarkan panjang string. (Dipindahkan dari mode_windows.py)"""
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