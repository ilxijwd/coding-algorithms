import os
import tkinter as tk
from tkinter.ttk import LabelFrame, Label, Entry, Combobox, Button, Treeview
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mb
from helpers import load_appearances, generate_appearances, calculate_entropy, calculate_compression
from shennon import shennon_code
from huffman import huffman_code
from convolutional import message_to_int_array, generate_polynoms, convolutional_code
from hemming import slice_message_to_int, slice_message_to_str, hemming_encoding

# GLOBALS #
APPEARANCES = {}
ALPHABET_MAP = {}
CODES = {}
ENTROPY = 0
COMPRESSION = 0
N = 0
K = 0
CORRECTED_CODE = ""
###########

window = tk.Tk()
window.title("ТІК КН-3.01")
window.resizable(False, False)

############################################################
data_frame = LabelFrame(window, text="Початкова інформація")

Label(data_frame, text="Повідомлення").grid(padx=10, pady=5)
message_entry = tk.Text(data_frame, width=50, height=10)
message_entry.grid(padx=10, pady=5)

Label(data_frame, text="Тип алгоритму").grid(padx=10, pady=5)
code_algorithms = Combobox(data_frame, state="readonly", values=("Хаффман", "Шеннон-Фано"))
code_algorithms.current(0)
code_algorithms.grid(padx=10, pady=5)

data_frame.grid(row=0, column=0, padx=10, pady=10)
############################################################
############################################################
alphabet_frame = LabelFrame(window, text="Абетка значень")


def cleanup_alphabet_frame():
    alphabet_table.delete(*alphabet_table.get_children())
    file_path_entry.configure(state="normal")
    file_path_entry.delete(0, tk.END)
    file_path_entry.configure(state="readonly")
    change_file_button.configure(state="disabled")


def change_table_data(filename):
    global APPEARANCES
    cleanup_alphabet_frame()
    change_file_button.configure(state="normal")
    file_path_entry.configure(state="normal")
    file_path_entry.insert(0, filename)
    file_path_entry.configure(state="readonly")
    try:
        APPEARANCES = load_appearances(filename)
        for (letter, value) in APPEARANCES.items():
            alphabet_table.insert("", "end", values=(letter, value))
    except:
        cleanup_alphabet_frame()
        mb.showerror("Невірні дані", "Неможливо розпарсити алфавіт файлу JSON")


def upload_file():
    filename = askopenfilename(initialdir="/", title="Виберіть алфавітний файл", filetypes=(("JSON файл", "*.json"),))
    if not filename:
        return
    change_table_data(filename)


def open_alphabet_file():
    filename = file_path_entry.get()
    if filename[-5:] == ".json":
        os.system(f"notepad.exe {filename}")
    change_table_data(filename)


upload_file_button = Button(alphabet_frame, text="Завантажити з JSON файлу", cursor="hand2", command=upload_file)
upload_file_button.grid(row=0, column=0, padx=10, pady=5)

change_file_button = Button(alphabet_frame, text="Змінити вміст JSON файлу", state="disabled", cursor="hand2",
                            command=open_alphabet_file)
change_file_button.grid(row=0, column=1, padx=10, pady=5)

file_path_entry = Entry(alphabet_frame, state="readonly", width=50)
file_path_entry.grid(row=1, columnspan=2, padx=10, pady=5)

alphabet_table_columns = ("Буква", "Ймовірність")
alphabet_table = Treeview(alphabet_frame, columns=alphabet_table_columns, show="headings")
for col in alphabet_table_columns:
    alphabet_table.heading(col, text=col)

alphabet_table.grid(row=2, columnspan=2, padx=10, pady=5)

alphabet_frame.grid(row=1, column=0, padx=10, pady=10)
############################################################
############################################################
appearances_frame = LabelFrame(window, text="Таблиця ймовірностей")

appearances_table_columns = ("Буква", "Ймовірність")
appearances_table = Treeview(appearances_frame, columns=appearances_table_columns, show="headings")
for col in appearances_table_columns:
    appearances_table.heading(col, text=col)

appearances_table.pack(padx=10, pady=5)


def cleanup_appearances_frame():
    appearances_table.delete(*appearances_table.get_children())


def fill_appearances_table():
    global ALPHABET_MAP
    cleanup_appearances_frame()

    message = message_entry.get("1.0", tk.END).upper().rstrip("\n")
    appearances_map = generate_appearances(message, APPEARANCES)
    sorted_alphabet = sorted(set(message), key=lambda letter: appearances_map[letter], reverse=True)
    ALPHABET_MAP = {letter: appearances_map[letter] for letter in sorted_alphabet}

    for (letter, value) in ALPHABET_MAP.items():
        appearances_table.insert("", "end", values=(letter, value))


calculate_appearances_button = Button(appearances_frame, text="Розрахувати", cursor="hand2", command=fill_appearances_table)
calculate_appearances_button.pack(padx=10, pady=5)

appearances_frame.grid(row=0, column=1, padx=10, pady=10)
############################################################
############################################################
codes_frame = LabelFrame(window, text="Таблиця кодів")

codes_table_columns = ("Буква", "Код")
codes_table = Treeview(codes_frame, columns=codes_table_columns, show="headings")
for col in codes_table_columns:
    codes_table.heading(col, text=col)

codes_table.pack(padx=10, pady=5)


def cleanup_codes_frame():
    codes_table.delete(*codes_table.get_children())


def fill_codes_table():
    global CODES
    cleanup_codes_frame()

    code_algorithm = code_algorithms.get().lower()

    if code_algorithm == "хаффман":
        CODES = huffman_code(ALPHABET_MAP)
    elif code_algorithm == "шеннон-фано":
        CODES = shennon_code(ALPHABET_MAP)

    for (letter, value) in CODES.items():
        codes_table.insert("", "end", values=(letter, value))


calculate_codes_button = Button(codes_frame, text="Розрахувати", cursor="hand2", command=fill_codes_table)
calculate_codes_button.pack(padx=10, pady=5)

codes_frame.grid(row=1, column=1, padx=10, pady=10)
############################################################
############################################################
result_frame = LabelFrame(window, text="Результати роботи")

Label(result_frame, text="Кодове повідомлення").pack(padx=10, pady=5)
code_entry = tk.Text(result_frame, state="disabled", width=50, height=10)
code_entry.pack(padx=10, pady=5)


def cleanup_result_frame():
    code_entry.configure(state="normal")
    code_entry.delete("1.0", tk.END)
    code_entry.configure(state="disabled")


def encode_message():
    global CODES
    cleanup_result_frame()

    message = message_entry.get("1.0", tk.END).upper().rstrip("\n")
    code_entry.configure(state="normal")
    code_entry.insert("1.0", "".join((CODES[letter] for letter in message)))
    code_entry.configure(state="disabled")


encode_button = Button(result_frame, text="Розрахувати", cursor="hand2", command=encode_message)
encode_button.pack(padx=10, pady=5)

result_frame.grid(row=0, column=2, padx=10, pady=10)
############################################################
############################################################
correction_code_frame = LabelFrame(window, text="Коректування коду")

Label(correction_code_frame, text="Коректувальний код").grid(row=0, column=0, padx=10, pady=5)
correction_code_algorithms = Combobox(correction_code_frame, state="readonly", values=("Хеммінг", "Згортковий", "Циклічний"))
correction_code_algorithms.current(0)
correction_code_algorithms.grid(row=0, column=1, padx=10, pady=5)

Label(correction_code_frame, text="n").grid(row=1, column=0, padx=10, pady=5)
n_entry = Entry(correction_code_frame)
n_entry.grid(row=1, column=1, padx=10, pady=5)

Label(correction_code_frame, text="k").grid(row=2, column=0, padx=10, pady=5)
k_entry = Entry(correction_code_frame)
k_entry.grid(row=2, column=1, padx=10, pady=5)

Label(correction_code_frame, text="Коректованнй код").grid(row=3, columnspan=2, padx=10, pady=5)
corrected_code = tk.Text(correction_code_frame, state="disabled", width=50, height=10)
corrected_code.grid(row=4, columnspan=2, padx=10, pady=5)


def cleanup_corrected_code_frame():
    corrected_code.configure(state="normal")
    corrected_code.delete("1.0", tk.END)
    corrected_code.configure(state="disabled")


def correct_code_message():
    global CORRECTED_CODE, N, K
    cleanup_corrected_code_frame()

    N = int(n_entry.get())
    K = int(k_entry.get())
    encoded_message = code_entry.get("1.0", tk.END).upper().rstrip("\n")
    correction_code = correction_code_algorithms.get().lower()

    if correction_code == 'хеммінг':
        chunks = slice_message_to_int(encoded_message, K)
        CORRECTED_CODE = hemming_encoding(chunks, N)
    elif correction_code == 'згортковий':
        top_conn, bottom_conn = generate_polynoms(N, K)
        CORRECTED_CODE = convolutional_code(top_conn, bottom_conn, message_to_int_array(encoded_message))
    elif correction_code == 'циклічний':
        pass

    corrected_code.configure(state="normal")
    corrected_code.insert("1.0", CORRECTED_CODE)
    corrected_code.configure(state="disabled")


correct_code_button = Button(correction_code_frame, text="Розрахувати", cursor="hand2", command=correct_code_message)
correct_code_button.grid(row=5, columnspan=2, padx=10, pady=5)

correction_code_frame.grid(row=1, column=2, padx=10, pady=10)
############################################################
window.mainloop()
