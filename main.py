import tkinter as tk
from basic_mode import start_basic
from function_mode import start_function

# === WARNA UTAMA ===
BG_UTAMA = "#000000"
BTN_KUNING = "#FFB800"
TEXT_WARNA = "black"

def main_menu(root):
    """Menampilkan menu utama kalkulator"""
    for w in root.winfo_children():
        w.destroy()

    root.title("Kalkulator Serbaguna")
    root.config(bg=BG_UTAMA)

    # Judul
    tk.Label(
        root,
        text="Pilih Mode Kalkulator",
        font=("Consolas", 26, "bold"),
        bg=BG_UTAMA,
        fg="white",
        pady=40
    ).pack()

    # Fungsi pembuat tombol
    def buat_tombol(teks, fungsi):
        return tk.Button(
            root, text=teks, command=fungsi,
            font=("Arial", 18, "bold"),
            bg=BTN_KUNING, fg=TEXT_WARNA,
            activebackground="#FFD633",
            activeforeground="black",
            width=20, height=2, bd=0,
            relief="flat", highlightthickness=0
        )

    frame = tk.Frame(root, bg=BG_UTAMA)
    frame.pack(pady=30)

    # 4 pilihan menu
    buat_tombol("🧮  Basic", lambda: start_basic(root, lambda: main_menu(root))).pack(pady=10)
    buat_tombol("📐  Function", lambda: start_function(root, lambda: main_menu(root))).pack(pady=10)
    buat_tombol("🔤  Multi (Coming Soon)", lambda: print("Mode Multi belum aktif")).pack(pady=10)
    buat_tombol("⚖️  BMI (Coming Soon)", lambda: print("Mode BMI belum aktif")).pack(pady=10)

    tk.Label(
        root,
        text="Kalkulator UAS - Python Project",
        bg=BG_UTAMA,
        fg="gray",
        font=("Arial", 10)
    ).pack(side="bottom", pady=15)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("480x620")
    main_menu(root)
    root.mainloop()
