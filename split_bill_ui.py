import tkinter as tk

from tkinter import messagebox, ttk

import re

from collections import defaultdict



# Import konstanta (Fallbacks)

try:

    from konstanta import BG_COLOR, FG_COLOR, TEXT_COLOR, ENTRY_BG, BTN_COLOR_ACCENT, BTN_COLOR_NORMAL

except ImportError:

    BG_COLOR = "#292929"

    FG_COLOR = "#FF9800"

    TEXT_COLOR = "#CCCCCC"

    ENTRY_BG = "#444444"

    BTN_COLOR_ACCENT = "#555555"

    BTN_COLOR_NORMAL = "#3A3A3A"



class SplitBillFrame(tk.Frame):

    def __init__(self, parent, return_to_menu):

        tk.Frame.__init__(self, parent, bg=BG_COLOR)

        self.return_to_menu = return_to_menu

        self.item_entries = []

        # Mengatur default awal 3 orang

        self.people_names = [f"Orang {i+1}" for i in range(3)] 

        

        self.setup_header()

        

        # --- FRAME UTAMA UNTUK INPUT DAN SCROLL ---

        self.main_content_canvas = tk.Canvas(self, bg=BG_COLOR, bd=0, highlightthickness=0)

        self.main_content_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.main_content_canvas.yview)

        self.scrollable_content_frame = tk.Frame(self.main_content_canvas, bg=BG_COLOR, padx=10)



        self.scrollable_content_frame.bind(

            "<Configure>",

            lambda e: self.main_content_canvas.configure(

                scrollregion=self.scrollable_content_frame.bbox("all")

            )

        )



        self.window_item_id = self.main_content_canvas.create_window((0, 0), window=self.scrollable_content_frame, anchor="nw", width=self.winfo_width())

        self.main_content_canvas.configure(yscrollcommand=self.main_content_scrollbar.set)

        

        self.bind("<Configure>", self.on_frame_resize) 



        self.main_content_canvas.pack(side="left", fill="both", expand=True, pady=(5,0))

        self.main_content_scrollbar.pack(side="right", fill="y", pady=(5,0))

        # --- END FRAME UTAMA ---



        # Panggil Setup di dalam scrollable_content_frame

        self.setup_people_control(self.scrollable_content_frame)

        self.setup_menu_table(self.scrollable_content_frame)

        

        # Panggil setup tombol tambah/hapus di luar frame tabel

        self.setup_table_control_buttons(self.scrollable_content_frame) 

        

        self.setup_discount_block(self.scrollable_content_frame)

        self.setup_extra_fee_block(self.scrollable_content_frame)

        self.setup_result_area(self.scrollable_content_frame)

        

        # Tombol Hitung dipindahkan ke sini

        self.setup_calculate_button(self.scrollable_content_frame)

        

        # Tambahkan 3 baris item menu saat inisialisasi

        for _ in range(3):

            self.add_item_row()

            

        # Panggil Hitung untuk inisialisasi Total Bayar

        self.people_entry.insert(0, "3") 

        self.calculate_split(initial_run=True)





    def on_frame_resize(self, event):

        """Memastikan lebar window di Canvas selalu sama dengan lebar frame utama."""

        if self.window_item_id:

            # -20 untuk padding kiri dan kanan (jika ada padding pada canvas)

            self.main_content_canvas.itemconfig(self.window_item_id, width=event.width) 

        self.main_content_canvas.config(scrollregion=self.scrollable_content_frame.bbox("all"))



    def setup_header(self):

        header_frame = tk.Frame(self, bg=BG_COLOR)

        header_frame.pack(fill="x", padx=10, pady=(15, 5))

        

        back_btn = tk.Button(header_frame, text="←", font=("Segoe UI", 16, "bold"),

                             bg=BG_COLOR, fg=FG_COLOR, bd=0, 

                             activebackground=BTN_COLOR_ACCENT, activeforeground=FG_COLOR,

                             relief=tk.FLAT, padx=5, pady=5, 

                             command=self.return_to_menu)

        back_btn.pack(side="left") 

        

        title_label = tk.Label(header_frame, text="🧾 Pembagian Tagihan Rinci", font=("Segoe UI", 14, "bold"), 

                               bg=BG_COLOR, fg=FG_COLOR, anchor="center")

        title_label.pack(side="left", fill="x", expand=True) 



    def setup_calculate_button(self, parent_frame):

        # Tombol Hitung Ditempatkan di bawah input utama

        calculate_btn = tk.Button(parent_frame, text="HITUNG ULANG", command=self.calculate_split, 

                                  bg=FG_COLOR, fg=BG_COLOR, font=('Segoe UI', 12, 'bold'), 

                                  activebackground=BTN_COLOR_ACCENT, activeforeground=FG_COLOR, bd=0, relief=tk.FLAT, height=2)

        calculate_btn.pack(fill='x', padx=5, pady=(15, 10))





    def setup_people_control(self, parent_frame):

        # Jumlah Orang

        people_frame = tk.Frame(parent_frame, bg=ENTRY_BG, pady=10)

        people_frame.pack(fill='x', pady=(10, 5))

        

        tk.Label(people_frame, text="Jumlah Orang:", bg=ENTRY_BG, fg=TEXT_COLOR, font=("Segoe UI", 10, 'bold')).pack(side='left', padx=(10, 5))

        

        self.people_entry = tk.Entry(people_frame, bg=BTN_COLOR_NORMAL, fg="white", font=("Segoe UI", 10), bd=0, relief=tk.FLAT, width=5, insertbackground=FG_COLOR)

        self.people_entry.pack(side='left', ipady=4)

        

        self.people_entry.bind("<Return>", self.update_people_dropdowns)

        self.people_entry.bind("<FocusOut>", self.update_people_dropdowns)

        

        

    def setup_menu_table(self, parent_frame):

        # Label/Header Pesanan

        tk.Label(parent_frame, text="PESANAN & ALOKASI:", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10, 'bold'), anchor='w').pack(fill='x', pady=(10, 0))

        

        # Frame Tabel Item 

        table_frame = tk.Frame(parent_frame, bg=ENTRY_BG)

        table_frame.pack(fill='x', pady=(5, 0)) 



        # Header Tabel Item: Penyesuaian Lebar Kolom (8:2:1:2) -> Total 13 weight. Item Paling Dominan.

        header_labels = ["Item", "Harga Satuan", "Qty", "Dibayar Oleh"]

        

        # ITEM: 8 (Paling Dominan, ~61% ruang)

        table_frame.grid_columnconfigure(0, weight=8, minsize=100)

        # HARGA SATUAN: 2

        table_frame.grid_columnconfigure(1, weight=2, minsize=75)

        # QTY: 1 (Sangat Kecil)

        table_frame.grid_columnconfigure(2, weight=1, minsize=50) 

        # DIBAYAR OLEH: 2

        table_frame.grid_columnconfigure(3, weight=2, minsize=100)



        for col, text in enumerate(header_labels):

            tk.Label(table_frame, text=text, bg=ENTRY_BG, fg=FG_COLOR, font=("Segoe UI", 10, 'bold'), bd=1, relief=tk.FLAT).grid(row=0, column=col, sticky="nsew", padx=1, pady=1, ipady=5)

        

        self.item_table_frame = table_frame 

        self.current_item_row_index = 1 



    def setup_table_control_buttons(self, parent_frame):

        """Menyiapkan tombol Tambah/Hapus di luar frame tabel."""

        btn_frame = tk.Frame(parent_frame, bg=BG_COLOR, padx=10)

        btn_frame.pack(fill='x', pady=(5, 10))

        

        # Tombol Tambah

        add_btn = tk.Button(btn_frame, text="+ Tambah Item", command=self.add_item_row, 

                            bg=BTN_COLOR_NORMAL, fg=TEXT_COLOR, activebackground=BTN_COLOR_ACCENT, bd=0, relief=tk.FLAT, height=2)

        add_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))

        

        # Tombol Hapus

        remove_btn = tk.Button(btn_frame, text="— Hapus Terakhir", command=self.remove_item_row, 

                               bg=BTN_COLOR_NORMAL, fg=TEXT_COLOR, activebackground=BTN_COLOR_ACCENT, bd=0, relief=tk.FLAT, height=2)

        remove_btn.pack(side='right', fill='x', expand=True, padx=(5, 0))

        

        

    def setup_discount_block(self, parent_frame):

        # --- BLOK DISKON ---

        tk.Label(parent_frame, text="DISKON:", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10, 'bold'), anchor='w').pack(fill='x', pady=(10, 0))



        discount_frame = tk.Frame(parent_frame, bg=ENTRY_BG, pady=10)

        discount_frame.pack(fill='x', pady=(5, 10))

        

        tk.Label(discount_frame, text="Rp:", bg=ENTRY_BG, fg=TEXT_COLOR, font=("Segoe UI", 10, 'bold')).pack(side='left', padx=(10, 5))

        self.discount_entry = tk.Entry(discount_frame, bg=BTN_COLOR_NORMAL, fg="white", font=("Segoe UI", 10), bd=0, relief=tk.FLAT, width=15, insertbackground=FG_COLOR)

        self.discount_entry.insert(0, "0")

        self.discount_entry.bind("<KeyRelease>", lambda event, entry=self.discount_entry, is_int=False: self.format_entry(entry, is_int))

        self.discount_entry.pack(side='left', ipady=4)

        

    def setup_extra_fee_block(self, parent_frame):

        # --- BLOK BIAYA TAMBAHAN ---

        tk.Label(parent_frame, text="BIAYA TAMBAHAN:", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10, 'bold'), anchor='w').pack(fill='x', pady=(10, 0))



        extra_fee_frame = tk.Frame(parent_frame, bg=ENTRY_BG, pady=10)

        extra_fee_frame.pack(fill='x', pady=(5, 10))

        

        tk.Label(extra_fee_frame, text="Nama Biaya (Ongkir, dll):", bg=ENTRY_BG, fg=TEXT_COLOR).pack(side='left', padx=(10, 5))

        self.extra_fee_name_entry = tk.Entry(extra_fee_frame, bg=BTN_COLOR_NORMAL, fg="white", font=("Segoe UI", 10), bd=0, relief=tk.FLAT, width=15, insertbackground=FG_COLOR)

        self.extra_fee_name_entry.insert(0, "Ongkir")

        self.extra_fee_name_entry.pack(side='left', ipady=4)



        tk.Label(extra_fee_frame, text="Rp:", bg=ENTRY_BG, fg=TEXT_COLOR, font=("Segoe UI", 10, 'bold')).pack(side='left', padx=(10, 5))

        self.extra_fee_entry = tk.Entry(extra_fee_frame, bg=BTN_COLOR_NORMAL, fg="white", font=("Segoe UI", 10), bd=0, relief=tk.FLAT, width=10, insertbackground=FG_COLOR)

        self.extra_fee_entry.insert(0, "0")

        self.extra_fee_entry.bind("<KeyRelease>", lambda event, entry=self.extra_fee_entry, is_int=False: self.format_entry(entry, is_int))

        self.extra_fee_entry.pack(side='left', ipady=4)



    def setup_result_area(self, parent_frame):

        # --- BLOK HASIL AKHIR ---

        result_frame = tk.Frame(parent_frame, bg=BG_COLOR, pady=10)

        result_frame.pack(fill='x', pady=(10, 20))



        # 1. Total Bayar (Net)

        tk.Label(result_frame, text="Total yang harus dibayar (NET):", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10, 'bold')).pack(fill='x', anchor='w')

        self.final_bill_var = tk.StringVar(value="Rp 0")

        tk.Label(result_frame, textvariable=self.final_bill_var, bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 18, 'bold'), anchor='e').pack(fill='x', pady=(0, 10))

        

        # 2. Rincian Per Orang

        tk.Label(result_frame, text="Rincian Tagihan Per Orang:", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10, 'bold'), anchor='w').pack(fill='x', pady=(5, 2))

        

        self.detail_result_frame = tk.Frame(result_frame, bg=ENTRY_BG, padx=5, pady=5)

        self.detail_result_frame.pack(fill='x')

        

        self.update_result_display({}) 





    def update_people_dropdowns(self, event=None):

        try:

            num_people = int(self.people_entry.get().replace('.', ''))

            if num_people <= 0 or num_people > 100: 

                raise ValueError

            

            new_people_names = [f"Orang {i+1}" for i in range(num_people)]

            self.people_names = new_people_names + ["Semua"]

            

            # Index 3 adalah ComboBox di versi ini

            for row in self.item_entries:

                dropdown = row[3] 

                dropdown['values'] = self.people_names

                if dropdown.get() in [f"Orang {i+1}" for i in range(101)] and dropdown.get() not in self.people_names:

                    dropdown.set(self.people_names[-1])

                    

            self.update_result_display({})

            self.calculate_split(initial_run=True)

            

        except ValueError:

            current_num = len(self.people_names) - 1 if "Semua" in self.people_names else len(self.people_names)

            self.people_entry.delete(0, tk.END)

            self.people_entry.insert(0, str(current_num))

            messagebox.showwarning("Input Error", "Jumlah orang harus angka valid (1-100).")

            

    def format_entry(self, entry_widget, is_integer=False):

        """Memformat input entry agar hanya angka dan menambahkan pemisah ribuan."""

        try:

            current_text = entry_widget.get().replace('.', '') 

            if not current_text: return

            

            cleaned_text = re.sub(r'[^0-9,]', '', current_text)



            if is_integer:

                if not cleaned_text: cleaned_text = "0"

                value = int(cleaned_text.split(',')[0])

                formatted_value = f"{value:,.0f}".replace(',', '.')

            else:

                if ',' in cleaned_text:

                    parts = cleaned_text.split(',')

                    integer_part = re.sub(r'[^0-9]', '', parts[0])

                    decimal_part = re.sub(r'[^0-9]', '', parts[1])[:2]

                    

                    if integer_part == '': integer_part = '0'

                    

                    formatted_integer_part = f"{int(integer_part):,.0f}".replace(',', '.')

                    formatted_value = formatted_integer_part

                    

                    if parts[1] or current_text.endswith(','): 

                        formatted_value += "," + decimal_part

                else:

                    if not cleaned_text: cleaned_text = "0"

                    value = int(cleaned_text)

                    formatted_value = f"{value:,.0f}".replace(',', '.')



            entry_widget.delete(0, tk.END)

            entry_widget.insert(0, formatted_value)

            

        except ValueError:

            pass

        except Exception:

            pass



    def add_item_row(self):

        current_row = self.current_item_row_index + len(self.item_entries)

        table_frame = self.item_table_frame

        entry_data = []

        

        # 0: Nama Item (Item yang Dipesan)

        e0 = tk.Entry(table_frame, bg=ENTRY_BG, fg=TEXT_COLOR, font=("Segoe UI", 10), bd=0, relief=tk.FLAT, insertbackground=FG_COLOR)

        e0.grid(row=current_row, column=0, sticky="nsew", padx=1, pady=1)

        entry_data.append(e0)



        # 1: Harga Satuan 

        e1 = tk.Entry(table_frame, bg=BTN_COLOR_NORMAL, fg="white", font=("Segoe UI", 10), bd=0, relief=tk.FLAT, insertbackground=FG_COLOR)

        e1.insert(0, "0")

        e1.bind("<KeyRelease>", lambda event, entry=e1, is_int=False: self.format_entry(entry, is_int))

        e1.grid(row=current_row, column=1, sticky="nsew", padx=1, pady=1)

        entry_data.append(e1)



        # 2: Kuantitas (Qty) 

        e2 = tk.Entry(table_frame, bg=BTN_COLOR_NORMAL, fg="white", font=("Segoe UI", 10), bd=0, relief=tk.FLAT, insertbackground=FG_COLOR)

        e2.insert(0, "1")

        e2.bind("<KeyRelease>", lambda event, entry=e2, is_int=True: self.format_entry(entry, is_int))

        e2.grid(row=current_row, column=2, sticky="nsew", padx=1, pady=1)

        entry_data.append(e2)



        # 3: Dibayar Oleh (ComboBox) - Editable

        person_var = tk.StringVar(value=self.people_names[-1] if self.people_names else "")

        e3 = ttk.Combobox(table_frame, textvariable=person_var, values=self.people_names, font=("Segoe UI", 10)) 

        e3.set(self.people_names[-1] if self.people_names else "")

        e3.grid(row=current_row, column=3, sticky="nsew", padx=1, pady=1)

        entry_data.append(e3)



        self.item_entries.append(entry_data)

        

        self.scrollable_content_frame.update_idletasks()

        self.main_content_canvas.yview_moveto(1.0) # Scroll ke bawah

        



    def remove_item_row(self):

        # Biarkan minimal 1 baris item

        if len(self.item_entries) > 1:

            last_entry_row = self.item_entries.pop()

            for widget in last_entry_row: 

                widget.grid_forget()

                widget.destroy()

            self.calculate_split()



    def update_result_display(self, result_dict):

        # Bersihkan tampilan hasil sebelumnya

        for widget in self.detail_result_frame.winfo_children():

            widget.destroy()

            

        if not result_dict:

            tk.Label(self.detail_result_frame, text="Tekan HITUNG ULANG untuk melihat rincian.", bg=ENTRY_BG, fg="#888888", font=("Segoe UI", 10), anchor='w').pack(fill='x')

            return



        row = 0

        for person, cost in result_dict.items():

            formatted_cost = f"Rp {cost:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')

            

            # Label Nama

            tk.Label(self.detail_result_frame, text=f"• {person}:", bg=ENTRY_BG, fg=TEXT_COLOR, font=("Segoe UI", 10), anchor='w').grid(row=row, column=0, sticky='w', padx=5, pady=2)

            

            # Label Biaya (Dibuat bold dan rata kanan)

            tk.Label(self.detail_result_frame, text=formatted_cost, bg=ENTRY_BG, fg=FG_COLOR, font=("Segoe UI", 12, 'bold'), anchor='e').grid(row=row, column=1, sticky='e', padx=5, pady=2)

            row += 1

            

        self.detail_result_frame.grid_columnconfigure(1, weight=1)



    def calculate_split(self, event=None, initial_run=False):

        try:

            # 1. Ambil Input Utama dan Pre-check

            num_people_int = int(self.people_entry.get().replace('.', ''))

            discount = float(self.discount_entry.get().replace('.', '').replace(',', '.'))

            extra_fee = float(self.extra_fee_entry.get().replace('.', '').replace(',', '.'))

            

            if num_people_int <= 0:

                if not initial_run: messagebox.showerror("Error", "Jumlah orang harus lebih dari nol.")

                return



            # 2. Inisialisasi Akumulator

            person_costs = defaultdict(float)

            total_items_cost = 0.0

            total_item_cost_per_person = defaultdict(float) 



            # 3. Alokasikan Biaya Item per Orang (Index: 0:Item, 1:Harga, 2:Qty, 3:Orang)

            for row in self.item_entries:

                try:

                    price_str = row[1].get().replace('.', '').replace(',', '.') 

                    qty_str = row[2].get().replace('.', '') 

                    person_selection = row[3].get().strip()

                    

                    if not person_selection: 

                        person_selection = "Semua" 

                    

                    price = float(price_str) if price_str else 0.0

                    qty = int(qty_str) if qty_str else 0

                        

                    item_total = price * qty

                    total_items_cost += item_total

                    

                    # Logika Alokasi Biaya Item Murni

                    active_people = [name for name in self.people_names if name != "Semua"]

                    

                    if person_selection == "Semua":

                        cost_share = item_total / num_people_int

                        for person_name in active_people: 

                            person_costs[person_name] += cost_share

                            total_item_cost_per_person[person_name] += cost_share

                    else:

                        # Dialokasikan ke NAMA yang diketik/dipilih

                        person_costs[person_selection] += item_total

                        total_item_cost_per_person[person_selection] += item_total



                except ValueError:

                    if not initial_run: messagebox.showwarning("Input Item Invalid", f"Item tidak valid. Pastikan Harga dan Qty adalah angka yang benar.")

                    return 



            # 4. Alokasikan Diskon dan Biaya Tambahan (Proporsional)

            net_items_cost = total_items_cost - discount

            final_bill_total = net_items_cost + extra_fee

            

            if total_items_cost > 0:

                discount_rate = discount / total_items_cost

                extra_fee_rate = extra_fee / total_items_cost if extra_fee > 0 else 0

                

                # Kita perlu mengalokasikan ke SEMUA nama yang muncul di total_item_cost_per_person

                for person in total_item_cost_per_person.keys():

                    item_cost_murni = total_item_cost_per_person[person]

                    

                    discount_allocated = item_cost_murni * discount_rate

                    extra_fee_allocated = item_cost_murni * extra_fee_rate

                    

                    person_final_cost = item_cost_murni - discount_allocated + extra_fee_allocated

                    

                    person_costs[person] = person_final_cost

                    if person_costs[person] < 0: person_costs[person] = 0.0

            else:

                 # Jika total biaya item 0, bagi diskon/biaya tambahan secara rata ke nama default

                 discount_per_person = discount / num_people_int

                 extra_fee_per_person = extra_fee / num_people_int

                 

                 for person in [name for name in self.people_names if name != "Semua"]:

                     person_costs[person] = -discount_per_person + extra_fee_per_person

                     if person_costs[person] < 0: person_costs[person] = 0.0



            # 5. Tampilkan Hasil

            self.update_result_display(person_costs)

            

            formatted_final_bill = f"Rp {final_bill_total:,.0f}".replace(',', '_').replace('.', ',').replace('_', '.')

            self.final_bill_var.set(formatted_final_bill)



        except ValueError:

            if not initial_run: messagebox.showerror("Input Error", "Masukkan angka yang valid di semua kolom input.")

            self.update_result_display({})

        except Exception as e:

            if not initial_run: messagebox.showerror("Error", f"Terjadi kesalahan tak terduga: {e}")

            self.update_result_display({})

            

if __name__ == '__main__':

    # Untuk pengujian independen

    root = tk.Tk()

    root.title("Split Bill Test")

    root.geometry("500x700")

    

    main_container = tk.Frame(root, bg=BG_COLOR)

    main_container.pack(fill="both", expand=True)

    

    def back_to_menu():

        print("Kembali ke Menu dipanggil")

        root.destroy()

        

    split_frame = SplitBillFrame(main_container, back_to_menu)

    split_frame.pack(fill="both", expand=True)

    

    root.mainloop()