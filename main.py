import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

# --- Настройки ---
HISTORY_FILE = "history.json
MIN_LENGTH = 4
MAX_LENGTH = 32

# --- Функции работы с историей ---
def load_history():
    """Загружает историю из файла JSON при запуске."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_history():
    """Сохраняет историю в файл JSON при выходе или добавлении нового пароля."""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history_data, f, indent=4)

# --- Основная логика приложения ---
def generate_password():
    """Генерирует пароль на основе выбранных настроек."""
    try:
        length = int(length_var.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Длина пароля должна быть целым числом.")
        return

    # Проверка длины пароля
    if length < MIN_LENGTH or length > MAX_LENGTH:
        messagebox.showerror("Ошибка", f"Длина должна быть от {MIN_LENGTH} до {MAX_LENGTH} символов.")
        return

    # Проверка, что выбран хотя бы один тип символов
    if not (lower_var.get() or upper_var.get() or digits_var.get() or symbols_var.get()):
        messagebox.showwarning("Предупреждение", "Выберите хотя бы один тип символов.")
        return

    # Сбор набора символов для генерации
    chars = ''
    if lower_var.get(): chars += string.ascii_lowercase
    if upper_var.get(): chars += string.ascii_uppercase
    if digits_var.get(): chars += string.digits
    if symbols_var.get(): chars += string.punctuation

    password = ''.join(random.choices(chars, k=length))
    
    # Отображение и сохранение
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    
    history_data.append(password)
    update_history_table()
    save_history()

def copy_to_clipboard():
    """Копирует сгенерированный пароль в буфер обмена."""
    password = password_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")

def update_history_table():
    """Обновляет виджет таблицы истории."""
    for i in tree.get_children():
        tree.delete(i)
    for idx, pwd in enumerate(history_data):
        tree.insert("", "end", values=(idx+1, pwd))

# --- Инициализация данных ---
history_data = load_history()

# --- Создание окна ---
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("600x450")
root.resizable(False, False)

# --- Элементы интерфейса ---
# Длина пароля (Ползунок)
length_label = ttk.Label(root, text="Длина пароля:")
length_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
length_var = tk.IntVar(value=12)
length_slider = ttk.Scale(root, from_=MIN_LENGTH, to=MAX_LENGTH, variable=length_var, orient='horizontal', length=250)
length_slider.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

# Чекбоксы для выбора символов
options_frame = ttk.LabelFrame(root, text="Состав пароля")
options_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="we")

lower_var = tk.BooleanVar(value=True)
upper_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=False)

ttk.Checkbutton(options_frame, text="A-Z (Большие)", variable=upper_var).grid(row=0, column=0, sticky="w")
ttk.Checkbutton(options_frame, text="a-z (Маленькие)", variable=lower_var).grid(row=1, column=0, sticky="w")
ttk.Checkbutton(options_frame, text="0-9 (Цифры)", variable=digits_var).grid(row=0, column=1, sticky="w")
ttk.Checkbutton(options_frame, text="!@#$% (Символы)", variable=symbols_var).grid(row=1, column=1, sticky="w")

# Кнопка генерации и поле вывода
btn_frame = ttk.Frame(root)
btn_frame.grid(row=2, column=0, columnspan=3, pady=10)

ttk.Button(btn_frame, text="Сгенерировать", command=generate_password).pack(side="left", padx=5)
password_entry = ttk.Entry(btn_frame, width=45)
password_entry.pack(side="left", padx=5)
ttk.Button(btn_frame, text="Копировать", command=copy_to_clipboard).pack(side="left", padx=5)

# Таблица истории
history_frame = ttk.LabelFrame(root, text="История (сохраняется в history.json)")
history_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="nsew")

columns = ("id", "password")
tree = ttk.Treeview(history_frame, columns=columns, show="headings")
tree.heading("id", text="№")
tree.heading("password", text="Пароль")
tree.column("id", width=40)
tree.column("password", width=480)
tree.pack(fill="both", expand=True)

# Обновляем таблицу при запуске приложения
update_history_table()

# Запуск приложения
root.mainloop()
