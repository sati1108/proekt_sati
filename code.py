import tkinter as tk
from tkinter import ttk, messagebox
import random
import json

# Предопределённые задачи
tasks = [
    {"task": "Прочитать статью", "type": "учёба"},
    {"task": "Сделать зарядку", "type": "спорт"},
    {"task": "Отправить письмо", "type": "работа"},
]

history = []

# Загрузка истории из файла
def load_history():
    global history
    try:
        with open('history.json', 'r', encoding='utf-8') as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

# Сохранение истории
def save_history():
    with open('history.json', 'w', encoding='utf-8') as f:
        json.dump(history, f)

# Генерация задачи
def generate_task():
    if not filtered_tasks:
        messagebox.showinfo("Информация", "Нет задач для выбранного фильтра.")
        return
    task = random.choice(filtered_tasks)
    history.append(task)
    history_listbox.insert(tk.END, task['task'])
    save_history()

# Обновление фильтра
def update_filter(*args):
    global filtered_tasks
    selected = filter_var.get()
    if selected == 'все':
        filtered_tasks = tasks
    else:
        filtered_tasks = [t for t in tasks if t['type'] == selected]

# Добавление новой задачи
def add_task():
    task_text = entry_task.get().strip()
    task_type = entry_type.get().strip()
    if task_text == '' or task_type == '':
        messagebox.showerror("Ошибка", "Пожалуйста, заполните оба поля.")
        return
    tasks.append({"task": task_text, "type": task_type})
    entry_task.delete(0, tk.END)
    entry_type.delete(0, tk.END)

load_history()

root = tk.Tk()
root.title("Random Task Generator")

# Фильтр
filter_var = tk.StringVar(value='все')
filter_menu = ttk.Combobox(root, textvariable=filter_var, values=['все', 'учёба', 'спорт', 'работа'])
filter_menu.bind("<<ComboboxSelected>>", update_filter)
filter_menu.pack()

# Кнопка генерации
btn_generate = tk.Button(root, text="Сгенерировать задачу", command=generate_task)
btn_generate.pack()

# История
history_listbox = tk.Listbox(root, height=10, width=50)
history_listbox.pack()

# Новая задача
frame_new_task = tk.Frame(root)
frame_new_task.pack(pady=10)

tk.Label(frame_new_task, text="Задача:").grid(row=0, column=0)
entry_task = tk.Entry(frame_new_task)
entry_task.grid(row=0, column=1)

tk.Label(frame_new_task, text="Тип:").grid(row=1, column=0)
entry_type = tk.Entry(frame_new_task)
entry_type.grid(row=1, column=1)

btn_add = tk.Button(frame_new_task, text="Добавить задачу", command=add_task)
btn_add.grid(row=2, column=0, columnspan=2)

# Изначальный фильтр
filtered_tasks = tasks
update_filter()

root.mainloop()
