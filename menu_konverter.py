import tkinter as tk
from tkinter import ttk, messagebox
import time
from datetime import date, datetime 
from konstanta import *
from jendela_konverter_unit import UnitConverterWindow 

# Menggunakan try/except untuk mengimpor kelas konverter basis angka yang telah kita buat
try:
    from jendela_konverter_basis import NumberSystemConverterWindow
except ImportError:
    NumberSystemConverterWindow = None 

# ========================== DEFINISI UNIT LENGKAP ==============================
UNIT_DEFINITIONS = {
    # 1. PANJANG (Basis: Meter)
    "Panjang": {
        'Meter': {'symbol': 'm', 'factor': 1.0},
        'Sentimeter': {'symbol': 'cm', 'factor': 0.01},
        'Kilometer': {'symbol': 'km', 'factor': 1000.0},
        'Mil': {'symbol': 'mil', 'factor': 1609.34},
        'Kaki': {'symbol': 'ft', 'factor': 0.3048},
        'Inci': {'symbol': 'in', 'factor': 0.0254},
        'Basis': 'Meter',
        # Fungsi konversi khusus untuk penanganan non-linear 
        'is_complex': False,
    },
    # 2. MASSA (Basis: Kilogram)
    "Massa": {
        'Kilogram': {'symbol': 'kg', 'factor': 1.0},
        'Gram': {'symbol': 'g', 'factor': 0.001},
        'Miligram': {'symbol': 'mg', 'factor': 0.000001},
        'Pon': {'symbol': 'lb', 'factor': 0.453592},
        'Ons': {'symbol': 'oz', 'factor': 0.02835},
        'Ton (Metrik)': {'symbol': 't', 'factor': 1000.0},
        'Basis': 'Kilogram',
        'is_complex': False,
    },
    # 3. SUHU (Basis: Celcius) 
    "Suhu": {
        'Celcius': {'symbol': '°C', 'factor': 1.0}, # Dianggap basis 1.0
        'Fahrenheit': {'symbol': '°F', 'factor': 1.0},
        'Kelvin': {'symbol': 'K', 'factor': 1.0},
        'Reamur': {'symbol': '°R', 'factor': 1.0},
        'Basis': 'Celcius',
        'is_complex': True,
    },
    # 4. VOLUME (Basis: Meter Kubik)
    "Volume": {
        'Meter Kubik': {'symbol': 'm³', 'factor': 1.0},
        'Liter': {'symbol': 'L', 'factor': 0.001},
        'Mililiter': {'symbol': 'mL', 'factor': 0.000001},
        'Galon (US)': {'symbol': 'gal', 'factor': 0.00378541},
        'Kaki Kubik': {'symbol': 'ft³', 'factor': 0.0283168},
        'Basis': 'Meter Kubik',
        'is_complex': False,
    },
    # 5. DATA (Basis: Byte)
    "Data": {
        'Byte': {'symbol': 'B', 'factor': 1.0},
        'Kilobyte': {'symbol': 'KB', 'factor': 1024.0},
        'Megabyte': {'symbol': 'MB', 'factor': 1024.0**2},
        'Gigabyte': {'symbol': 'GB', 'factor': 1024.0**3},
        'Terabyte': {'symbol': 'TB', 'factor': 1024.0**4},
        'Bit': {'symbol': 'b', 'factor': 1/8},
        'Basis': 'Byte',
        'is_complex': False,
    },
    # 6. ENERGI (Basis: Joule)
    "Energi": {
        'Joule': {'symbol': 'J', 'factor': 1.0},
        'Kalori': {'symbol': 'Cal', 'factor': 4.184},
        'Kilojoule': {'symbol': 'kJ', 'factor': 1000.0},
        'Kilokalori': {'symbol': 'kCal', 'factor': 4184.0},
        'Basis': 'Joule',
        'is_complex': False,
    },
    # 7. DAYA (Basis: Watt)
    "Daya": {
        'Watt': {'symbol': 'W', 'factor': 1.0},
        'Kilowatt': {'symbol': 'kW', 'factor': 1000.0},
        'Horsepower (metrik)': {'symbol': 'HP', 'factor': 735.499},
        'Basis': 'Watt',
        'is_complex': False,
    },
    # 8. MATA UANG 
    "Mata Uang": {
        'Rupiah': {'symbol': 'IDR', 'factor': 1.0},
        'Dollar AS': {'symbol': 'USD', 'factor': 1/15500.0}, # Nilai Statis
        'Euro': {'symbol': 'EUR', 'factor': 1/17000.0},
        'Yen Jepang': {'symbol': 'JPY', 'factor': 1/100.0},
        'Basis': 'Rupiah',
        'is_complex': False,
    },
    # 9. AREA 
    "Area": {
        'Meter Persegi': {'symbol': 'm²', 'factor': 1.0},
        'Sentimeter Persegi': {'symbol': 'cm²', 'factor': 0.0001},
        'Hektar': {'symbol': 'ha', 'factor': 10000.0},
        'Kaki Persegi': {'symbol': 'ft²', 'factor': 0.092903},
        'Basis': 'Meter Persegi',
        'is_complex': False,
    },
    # 10. KECEPATAN 
    "Kecepatan": {
        'Meter/Detik': {'symbol': 'm/s', 'factor': 1.0},
        'Kilometer/Jam': {'symbol': 'km/j', 'factor': 1/3.6},
        'Mil/Jam': {'symbol': 'mph', 'factor': 0.44704},
        'Knot': {'symbol': 'knot', 'factor': 0.514444},
        'Basis': 'Meter/Detik',
        'is_complex': False,
    },
    # 11. TEKANAN 
    "Tekanan": {
        'Pascal': {'symbol': 'Pa', 'factor': 1.0},
        'Bar': {'symbol': 'bar', 'factor': 100000.0},
        'ATM': {'symbol': 'atm', 'factor': 101325.0},
        'PSI': {'symbol': 'psi', 'factor': 6894.76},
        'Basis': 'Pascal',
        'is_complex': False,
    },
    # 12. WAKTU 
    "Waktu": {
        'Detik': {'symbol': 'd', 'factor': 1.0},
        'Menit': {'symbol': 'm', 'factor': 60.0},
        'Jam': {'symbol': 'j', 'factor': 3600.0},
        'Hari': {'symbol': 'hr', 'factor': 86400.0},
        'Tahun': {'symbol': 'th', 'factor': 31536000.0}, # Tahun kalender (365 hari)
        'Basis': 'Detik',
        'is_complex': False,
    },
    # 13. USIA
    "Usia": {
        'Tahun': {'symbol': 't', 'factor': 1.0},
        'Bulan': {'symbol': 'b', 'factor': 1/12.0},
        'Minggu': {'symbol': 'mgg', 'factor': 1/52.143},
        'Hari': {'symbol': 'hr', 'factor': 1/365.0},
        'Basis': 'Tahun',
        'is_complex': False,
    }
}


# ========================== CONVERTER MENU CLASS ==============================
class ConverterUI(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Menu Konverter")
        self.configure(bg=BG_COLOR)
        self.geometry("380x680")
        self.resizable(True, True) 
        
        # Sembunyikan window utama
        self.master.withdraw()
        
        # Buat container frame utama
        self.main_container = tk.Frame(self, bg=BG_COLOR)
        self.main_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Style untuk scrollbar
        style = ttk.Style()
        style.configure("Converter.Vertical.TScrollbar",
                       background=BTN_COLOR_NORMAL,
                       troughcolor=BG_COLOR,
                       arrowcolor=TEXT_COLOR,
                       borderwidth=0)
        
        # Buat canvas dan scrollbar dalam container
        self.canvas = tk.Canvas(self.main_container, bg=BG_COLOR, 
                              highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(self.main_container, 
                                     orient="vertical",
                                     command=self.canvas.yview,
                                     style="Converter.Vertical.TScrollbar")
        
        # Frame yang dapat di-scroll
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_COLOR)
        self.scrollable_frame.bind("<Configure>", 
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Buat window dalam canvas dengan lebar yang mengikuti parent
        self._frame_id = self.canvas.create_window(
            (0, 0), 
            window=self.scrollable_frame,
            anchor="nw",
            width=self.canvas.winfo_width()  # Atur lebar awal
        )
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas dan scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y", padx=(2, 0))
        
        # Bind scroll events ke semua komponen utama
        for widget in (self, self.main_container, self.canvas, self.scrollable_frame):
            widget.bind("<MouseWheel>", self._on_mousewheel)
            # Bind untuk touch pad scroll di Linux/Mac
            widget.bind("<Button-4>", self._on_mousewheel)
            widget.bind("<Button-5>", self._on_mousewheel)
            
        # Bind window resize
        self.bind("<Configure>", self._on_window_resize)
        
        title = tk.Label(self.scrollable_frame, text="Converter", fg=FG_COLOR, bg=BG_COLOR,
                         font=("Segoe UI", 16, "bold"))
        title.pack(pady=15)
        
        # Bind scroll ke title juga
        title.bind("<MouseWheel>", self._on_mousewheel)

        grid_frame = tk.Frame(self.scrollable_frame, bg=BG_COLOR)
        grid_frame.pack(pady=(10, 0))
        
        # Setup scroll bindings awal
        self._setup_scroll_bindings()

        self.menu_items = [
            ("💪", "BMI", self.konversi_bmi), 
            ("🏷️", "Diskon", self.konversi_diskon), 
            ("📅", "Tanggal", self.konversi_tanggal), 
            ("🧓", "Usia", lambda: self.konversi_unit_umum("Usia")),
            ("📐", "Panjang", lambda: self.konversi_unit_umum("Panjang")), 
            ("⚖️", "Massa", lambda: self.konversi_unit_umum("Massa")), 
            ("🌡️", "Suhu", lambda: self.konversi_unit_umum("Suhu")), 
            ("📦", "Volume", lambda: self.konversi_unit_umum("Volume")), 
            ("💾", "Data", lambda: self.konversi_unit_umum("Data")), 
            ("🔋", "Energi", lambda: self.konversi_unit_umum("Energi")), 
            ("⚡", "Daya", lambda: self.konversi_unit_umum("Daya")), 
            ("💰", "Mata Uang", lambda: self.konversi_unit_umum("Mata Uang")), 
            ("📏", "Area", lambda: self.konversi_unit_umum("Area")), 
            ("🏎️", "Kecepatan", lambda: self.konversi_unit_umum("Kecepatan")), 
            ("🌪️", "Tekanan", lambda: self.konversi_unit_umum("Tekanan")), 
            ("⏰", "Waktu", lambda: self.konversi_unit_umum("Waktu")), 
            ("🕓", "Waktu UNIX", self.konversi_unix), 
            ("🔢", "Basis Angka", self.konversi_basis_angka), 
        ]

        cols = 3
        for i, (icon, name, func) in enumerate(self.menu_items):
            # Frame untuk satu menu item
            menu_frame = tk.Frame(grid_frame, bg=BG_COLOR)
            menu_frame.grid(row=i // cols, column=i % cols, padx=15, pady=20)
            
            # Icon
            icon_label = tk.Label(menu_frame, text=icon, fg=TEXT_COLOR, bg=BG_COLOR,
                                font=("Segoe UI Emoji", 22), cursor="hand2")
            icon_label.pack()
            
            # Text
            text_label = tk.Label(menu_frame, text=name, fg="#AAAAAA", bg=BG_COLOR,
                                font=("Segoe UI", 9), cursor="hand2")
            text_label.pack()
            
            # Simpan referensi ke labels untuk hover effect
            menu_frame.icon_label = icon_label
            menu_frame.text_label = text_label
            
            # Bind events untuk seluruh frame dan komponennya
            for widget in (menu_frame, icon_label, text_label):
                widget.bind("<Button-1>", lambda e, f=func: f())
                widget.bind("<Enter>", lambda e, frame=menu_frame: self._on_item_enter(frame))
                widget.bind("<Leave>", lambda e, frame=menu_frame: self._on_item_leave(frame))

        ttk.Button(self.scrollable_frame, text="Kembali", command=self.destroy).pack(pady=20)
        
        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _on_mousewheel(self, event):
        """Handle smooth scrolling dengan delta yang disesuaikan"""
        if self.canvas.winfo_height() < self.scrollable_frame.winfo_height():
            # Handle scroll untuk berbagai jenis event
            if event.num == 4:  # Linux/Mac scroll up
                delta = -1
            elif event.num == 5:  # Linux/Mac scroll down
                delta = 1
            else:  # Windows
                delta = -1 * (event.delta // 120)
            
            # Scroll dengan animasi halus
            self.canvas.yview_scroll(delta, "units")
            
            # Prevent event propagation
            return "break"

    def _on_window_resize(self, event):
        """Handle window resize untuk menyesuaikan lebar konten"""
        if event.widget == self:
            # Update canvas width
            new_width = event.width - self.scrollbar.winfo_width() - 12
            self.canvas.itemconfig(self._frame_id, width=new_width)
            
            # Update scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            # Rebind scroll events setelah resize
            self._setup_scroll_bindings()
        
    def _on_item_enter(self, frame):
        """Handle hover masuk ke item menu"""
        # Ubah warna semua komponen dalam frame
        frame.icon_label.configure(fg=FG_COLOR)
        frame.text_label.configure(fg=FG_COLOR)
        frame.configure(cursor="hand2")
        
    def _on_item_leave(self, frame):
        """Handle hover keluar dari item menu"""
        # Kembalikan warna semua komponen dalam frame
        frame.icon_label.configure(fg=TEXT_COLOR)
        frame.text_label.configure(fg="#AAAAAA")
        frame.configure(cursor="")

    def _setup_scroll_bindings(self):
        """Setup scroll bindings untuk semua widget yang perlu di-scroll"""
        # List semua widget yang perlu mendukung scrolling
        scrollable_widgets = [
            self,  # Main window
            self.main_container,  # Main container
            self.canvas,  # Canvas
            self.scrollable_frame,  # Scrollable frame
            *self.scrollable_frame.winfo_children()  # Semua child widgets
        ]
        
        # Bind scroll events ke semua widget
        for widget in scrollable_widgets:
            widget.bind("<MouseWheel>", self._on_mousewheel)
            widget.bind("<Button-4>", self._on_mousewheel)
            widget.bind("<Button-5>", self._on_mousewheel)
            
    def _add_back_button(self, parent, callback=None):
        """Menambahkan tombol kembali yang seragam ke window"""
        # Tambahkan tombol kembali hanya untuk window yang bukan UnitConverterWindow
        # karena UnitConverterWindow sudah memiliki tombol kembalinya sendiri
        if isinstance(parent, UnitConverterWindow):
            # Jika ini UnitConverterWindow, jangan tambahkan tombol lagi
            return
            
        # Buat frame untuk tombol
        button_frame = tk.Frame(parent, bg=BTN_COLOR_NORMAL)
        button_frame.pack(side="bottom", pady=20, fill="x")
        
        # Style untuk tombol kembali
        style = ttk.Style()
        style.configure("Back.TButton",
                       padding=10,
                       font=("Segoe UI", 10))
        
        # Tombol kembali
        back_btn = ttk.Button(
            button_frame,
            text="« Kembali",
            style="Back.TButton",
            command=callback if callback else parent.destroy
        )
        back_btn.pack()

    def destroy(self):
        """Override destroy method untuk menampilkan kembali window utama"""
        if self.master:
            self.master.deiconify()  # Tampilkan window utama
        super().destroy()

    # ==== Fungsi Generik untuk Konversi Unit ====
    def show_popup(self, popup_window):
        """Menampilkan popup window dan menyembunyikan window saat ini"""
        self.withdraw()  # Sembunyikan window konverter
        
        def on_popup_close():
            """Callback ketika popup ditutup"""
            popup_window.destroy()  # Tutup popup
            self.deiconify()  # Tampilkan kembali window konverter
        
        def on_back_button():
            """Callback untuk tombol kembali"""
            popup_window.destroy()  # Tutup popup
            self.deiconify()  # Tampilkan kembali window konverter
            
        # Tambahkan tombol kembali ke popup
        self._add_back_button(popup_window, callback=on_back_button)
            
        # Set protokol window closing
        popup_window.protocol("WM_DELETE_WINDOW", on_popup_close)
        
        return popup_window

    def konversi_unit_umum(self, category):
        """Membuka jendela konverter unit dengan semua pilihan satuan untuk kategori tertentu."""
        data = UNIT_DEFINITIONS.get(category)
        if data:
            # Buat window konverter
            converter = UnitConverterWindow(self, f"Konversi {category}", data)
            # Tampilkan sebagai popup
            self.show_popup(converter)
        else:
            messagebox.showerror("Error", f"Definisi unit untuk {category} tidak ditemukan.")

    # ==== Fungsi BMI (Menggunakan OptionMenu) ====

    def bmi_calculator_popup(self):
        win = tk.Toplevel(self)
        win.title("Hitung BMI Lanjut")
        win.configure(bg=BTN_COLOR_NORMAL)
        win.geometry("350x400")  # Tinggi ditambah untuk tombol kembali
        
        # Container untuk konten utama
        main_frame = tk.Frame(win, bg=BTN_COLOR_NORMAL)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(20,0))
        
        # Gunakan fitur popup
        self.show_popup(win)

        weight_var = tk.StringVar(value="")
        height_var = tk.StringVar(value="")
        weight_unit = tk.StringVar(value="Kilogram")
        height_unit = tk.StringVar(value="cm")
        
        weight_options = ["Kilogram", "Pon"]
        height_options = ["cm", "m", "Kaki", "Inci"]
        
        result_label = tk.Label(win, text="", fg=FG_COLOR, bg=BTN_COLOR_NORMAL)
        result_label.pack(pady=10)

        weight_frame = tk.Frame(win, bg=BTN_COLOR_NORMAL)
        weight_frame.pack(pady=(10, 0))
        tk.Label(weight_frame, text="Berat:", fg=TEXT_COLOR, bg=BTN_COLOR_NORMAL).pack(side=tk.LEFT)
        tk.Entry(weight_frame, textvariable=weight_var, bg=ENTRY_BG, fg=TEXT_COLOR, width=10).pack(side=tk.LEFT, padx=5)
        ttk.OptionMenu(weight_frame, weight_unit, weight_unit.get(), *weight_options).pack(side=tk.LEFT, padx=5)

        height_frame = tk.Frame(win, bg=BTN_COLOR_NORMAL)
        height_frame.pack(pady=(10, 0))
        tk.Label(height_frame, text="Tinggi:", fg=TEXT_COLOR, bg=BTN_COLOR_NORMAL).pack(side=tk.LEFT)
        tk.Entry(height_frame, textvariable=height_var, bg=ENTRY_BG, fg=TEXT_COLOR, width=10).pack(side=tk.LEFT, padx=5)
        ttk.OptionMenu(height_frame, height_unit, height_unit.get(), *height_options).pack(side=tk.LEFT, padx=5)

        def hitung():
            try:
                weight = float(weight_var.get())
                height = float(height_var.get())
                
                if weight_unit.get() == "Pon":
                    weight_kg = weight * 0.453592 
                else:
                    weight_kg = weight
                
                h_unit = height_unit.get()
                if h_unit == "cm":
                    height_m = height / 100
                elif h_unit == "Kaki":
                    height_m = height * 0.3048 
                elif h_unit == "Inci":
                    height_m = height * 0.0254 
                else: 
                    height_m = height
                
                if height_m <= 0:
                    raise ValueError("Tinggi tidak boleh nol.")

                bmi = weight_kg / (height_m ** 2)
                
                result_label.config(text=f"BMI: {round(bmi, 2)}")
                
            except ValueError:
                messagebox.showerror("Error", "Masukkan angka yang valid untuk berat dan tinggi.")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

        # Frame untuk tombol hitung
        btn_frame = tk.Frame(main_frame, bg=BTN_COLOR_NORMAL)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Hitung", command=hitung).pack()
    
    def konversi_bmi(self):
        self.bmi_calculator_popup()

    # ==== Fungsi Kalkulator Popup Generik ====

    def calculator_popup(self, title, labels, button_text, calculate_func):
        win = tk.Toplevel(self)
        win.title(title)
        win.configure(bg=BTN_COLOR_NORMAL)
        win.geometry("300x400")  # Tinggi ditambah untuk tombol kembali
        
        # Container untuk konten utama
        main_frame = tk.Frame(win, bg=BTN_COLOR_NORMAL)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(20,0))
        
        # Gunakan fitur popup
        self.show_popup(win)
        
        entries = []
        
        # Frame untuk input fields
        input_frame = tk.Frame(main_frame, bg=BTN_COLOR_NORMAL)
        input_frame.pack(fill="x", pady=10)
        
        for label_text in labels:
            label_frame = tk.Frame(input_frame, bg=BTN_COLOR_NORMAL)
            label_frame.pack(fill="x", pady=5)
            
            tk.Label(label_frame, text=label_text, 
                    fg=TEXT_COLOR, bg=BTN_COLOR_NORMAL,
                    font=("Segoe UI", 10)).pack(anchor="w")
            
            entry = tk.Entry(label_frame, bg=ENTRY_BG, fg=TEXT_COLOR,
                           font=("Segoe UI", 10))
            entry.pack(fill="x", pady=(5,0))
            entries.append(entry)
        
        # Frame untuk hasil
        result_frame = tk.Frame(main_frame, bg=BTN_COLOR_NORMAL)
        result_frame.pack(fill="x", pady=15)
        
        result_label = tk.Label(result_frame, text="", fg=FG_COLOR, 
                              bg=BTN_COLOR_NORMAL, font=("Segoe UI", 12))
        result_label.pack()

        def hitung():
            try:
                values = [e.get() for e in entries]
                hasil_text = calculate_func(*values)
                result_label.config(text=hasil_text)
            except ValueError as e:
                messagebox.showerror("Error", f"Format input salah. Detil: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

        # Frame untuk tombol hitung
        btn_frame = tk.Frame(main_frame, bg=BTN_COLOR_NORMAL)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text=button_text, command=hitung).pack()

    # --- IMPLEMENTASI FITUR POPUP ---

    def konversi_diskon(self):
        self.calculator_popup("Hitung Diskon", ["Harga (Rp):", "Diskon (%):"], "Hitung", 
            lambda h, d: f"Harga Akhir: Rp {round(float(h) - (float(h) * float(d) / 100), 2)}")

    def konversi_unix(self):
        self.calculator_popup("Waktu UNIX", ["Masukkan UNIX timestamp:"], "Konversi", 
            lambda t: f"Waktu: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(t)))}")

    def konversi_tanggal(self):
        def hitung_selisih_tanggal(tgl_awal_str, tgl_akhir_str):
            tgl_awal = datetime.strptime(tgl_awal_str, '%Y-%m-%d').date()
            tgl_akhir = datetime.strptime(tgl_akhir_str, '%Y-%m-%d').date()
            selisih = abs((tgl_akhir - tgl_awal).days)
            return f"Selisih: {selisih} hari"

        self.calculator_popup("Konversi Tanggal", 
            ["Tanggal Awal (YYYY-MM-DD):", "Tanggal Akhir (YYYY-MM-DD):"], 
            "Hitung Selisih", 
            hitung_selisih_tanggal)
            
    def konversi_basis_angka(self):
        if NumberSystemConverterWindow:
            converter = NumberSystemConverterWindow(self)
            self.show_popup(converter)
        else:
            messagebox.showerror("Error", "Kelas 'NumberSystemConverterWindow' (dari jendela_konverter_basis.py) tidak ditemukan.")
