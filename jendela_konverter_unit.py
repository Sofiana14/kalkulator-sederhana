import tkinter as tk
from tkinter import ttk
from konstanta import *
from utilitas import adjust_font_size

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


        # --- Keypad Kalkulator ---
        
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
            # Menggunakan fungsi konversi yang disediakan oleh data unit
            hasil = self.unit_data['conversion_func'](val)
            formatted_hasil = f"{hasil:.4f}".rstrip('0').rstrip('.')
            self.result_var.set(f"{formatted_hasil} {self.unit_data['to_unit_name']}")
            
            adjust_font_size(self.output_label, self.result_var, max_chars_small=16, max_chars_tiny=22, default_size=24)

        except ValueError:
             self.result_var.set(f"0 {self.unit_data['to_unit_name']}")
        except Exception:
             self.result_var.set("Error")