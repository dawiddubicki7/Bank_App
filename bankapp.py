import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os

# Baza danych
conn = sqlite3.connect('bank.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT NOT NULL UNIQUE,
             password TEXT NOT NULL,
             balance REAL DEFAULT 0)''')
conn.commit()

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def register():
    username = entry_reg_username.get()
    password = entry_reg_password.get()
    
    if username == "" or password == "":
        messagebox.showerror("Błąd", "Wszystkie pola są wymagane!")
        return
    
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchone():
        messagebox.showerror("Błąd", "Nazwa użytkownika jest już zajęta!")
        return
    
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    messagebox.showinfo("Sukces", "Rejestracja zakończona pomyślnie!")
    register_win.destroy()
    login_win.deiconify()  

def login():
    global current_user
    username = entry_login_username.get()
    password = entry_login_password.get()
    
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    
    if user:
        current_user = user
        login_win.destroy()
        create_main_window()
    else:
        messagebox.showerror("Błąd", "Nieprawidłowy login lub hasło")

def logout():
    global main_win
    main_win.destroy()
    create_login_window()

def deposit():
    global current_user
    try:
        amount = float(entry_amount.get())
    except ValueError:
        messagebox.showerror("Błąd", "Proszę wprowadzić prawidłową kwotę")
        return
    
    new_balance = current_user[3] + amount
    c.execute("UPDATE users SET balance=? WHERE id=?", (new_balance, current_user[0]))
    conn.commit()
    messagebox.showinfo("Sukces", f"Wpłacono {amount} zł. Nowe saldo: {new_balance} zł")
    current_user = (current_user[0], current_user[1], current_user[2], new_balance)

def withdraw():
    global current_user
    try:
        amount = float(entry_amount.get())
    except ValueError:
        messagebox.showerror("Błąd", "Proszę wprowadzić prawidłową kwotę")
        return
    
    if amount > current_user[3]:
        messagebox.showerror("Błąd", f"Niewystarczające środki na koncie.\nTwoje saldo wynosi: {current_user[3]} zł")
    else:
        new_balance = current_user[3] - amount
        c.execute("UPDATE users SET balance=? WHERE id=?", (new_balance, current_user[0]))
        conn.commit()
        messagebox.showinfo("Sukces", f"Wypłacono {amount} zł. Nowe saldo: {new_balance} zł")
        current_user = (current_user[0], current_user[1], current_user[2], new_balance)

def check_balance():
    global current_user
    messagebox.showinfo("Saldo", f"Twoje saldo wynosi: {current_user[3]} zł")

def set_background(window, image_path):
    image = Image.open(image_path)
    bg_image = ImageTk.PhotoImage(image)
    bg_label = tk.Label(window, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    return bg_image.width(), bg_image.height()

def open_register_window():
    global entry_reg_username, entry_reg_password, register_win
    login_win.withdraw()  
    register_win = tk.Toplevel(login_win)
    register_win.title("bank saturn - Rejestracja")
    current_directory = os.path.dirname(os.path.abspath(__file__)) + "\images\wejsciesaturnbank.png"
    width, height = set_background(register_win, current_directory)
    center_window(register_win, width, height)

    register_frame = tk.Frame(register_win, bg='white')
    register_frame.place(relx=0.5, rely=0.5, anchor='center')

    tk.Label(register_frame, text="Nazwa użytkownika").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_reg_username = tk.Entry(register_frame)
    entry_reg_username.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(register_frame, text="Hasło").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_reg_password = tk.Entry(register_frame, show="*")
    entry_reg_password.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(register_frame, text="Zarejestruj", command=register).grid(row=2, column=0, padx=10, pady=10, columnspan=2)
    tk.Button(register_frame, text="Powrót do logowania", command=lambda: [register_win.destroy(), login_win.deiconify()]).grid(row=3, column=0, padx=10, pady=10, columnspan=2)
    register_win.grab_set()  

def create_login_window():
    global entry_login_username, entry_login_password, login_win
    login_win = tk.Tk()
    login_win.title("bank saturn - Logowanie")
    current_directory = os.path.dirname(os.path.abspath(__file__)) + "\images\wejsciesaturnbank.png"
    width, height = set_background(login_win, current_directory)
    center_window(login_win, width, height)

    login_frame = tk.Frame(login_win, bg='white')
    login_frame.place(relx=0.5, rely=0.5, anchor='center')

    tk.Label(login_frame, text="Nazwa użytkownika").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_login_username = tk.Entry(login_frame)
    entry_login_username.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(login_frame, text="Hasło").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_login_password = tk.Entry(login_frame, show="*")
    entry_login_password.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(login_frame, text="Zaloguj", command=login).grid(row=2, column=0, padx=10, pady=10, columnspan=2)
    tk.Button(login_frame, text="Zarejestruj się", command=open_register_window).grid(row=3, column=0, padx=10, pady=10, columnspan=2)
    login_win.mainloop()

def create_main_window():
    global entry_amount, main_win
    main_win = tk.Tk()  
    main_win.title("bank saturn - Aplikacja Bankowa")
    current_directory = os.path.dirname(os.path.abspath(__file__)) + "\images\wnetrzebbanku.png"
    width, height = set_background(main_win, current_directory)
    center_window(main_win, width, height)

    main_frame = tk.Frame(main_win, bg='white')
    main_frame.place(relx=0.5, rely=0.5, anchor='center')

    tk.Label(main_frame, text="Kwota").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_amount = tk.Entry(main_frame)
    entry_amount.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(main_frame, text="Wpłać", command=deposit).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(main_frame, text="Wypłać", command=withdraw).grid(row=1, column=1, padx=10, pady=10)
    tk.Button(main_frame, text="Sprawdź saldo", command=check_balance).grid(row=2, column=0, padx=10, pady=10)
    tk.Button(main_frame, text="Wyloguj", command=logout).grid(row=2, column=1, padx=10, pady=10)

    main_win.mainloop()  

def start_window():
    create_login_window()

start_window()
