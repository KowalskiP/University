__author__ = 'kowalski'
from tkinter.filedialog import asksaveasfilename
import tkinter as tk
import sys

import config
import base.handler
import base.net
import base.text
import base.commands
import base.control
import base.new_CSR


def client_options_go(destination, window):
    """Запуск экземпляра клиента с настройками."""
    if base.control.check_options(window, destination):
        if not config.isCLI:
            window.destroy()
        base.new_CSR.Client(destination, config.port).start()
    elif config.isCLI:
        sys.exit(1)


def username_options_window(master):
    """Запуск окна смены ника."""
    config.top = tk.Toplevel(master)
    config.top.title("Настройки никнейма")
    config.top.grab_set()
    tk.Label(config.top, text="Никнейм:").grid(row=0)
    name = tk.Entry(config.top)
    name.focus_set()
    name.grid(row=0, column=1)
    go = tk.Button(config.top, text="Сменить", command=lambda:
                   username_options_go(name.get(), config.top))
    go.grid(row=1, column=1)


def username_options_go(name, window):
    """Отправка текстовой команды смены ника."""
    base.commands.user_commands("nick", [name])
    window.destroy()


def option_delete(window):
    window.destroy()


def contacts_connect(item):
    """Подключение к контакту из списка."""
    base.new_CSR.Client(item[1], int(item[2])).start()


def contacts_remove(item, listbox):
    """Удаление контакта."""
    if listbox.size() != 0:
        listbox.delete(tk.ACTIVE)
        config.contact_array.pop(item[1])


def contacts_add(listbox, master):
    """Добавление контакта."""
    window = tk.Toplevel(master)
    window.title("Добавление контакта")
    tk.Label(window, text="Ник:").grid(row=0)
    name = tk.Entry(window)
    name.focus_set()
    name.grid(row=0, column=1)
    tk.Label(window, text="IP:").grid(row=1)
    ip = tk.Entry(window)
    ip.grid(row=1, column=1)
    tk.Label(window, text="Порт:").grid(row=2)
    config.port = tk.Entry(window)
    config.port.grid(row=2, column=1)
    go = tk.Button(window, text="Добвать", command=lambda:
                   contacts_add_check(name.get(),
                   ip.get(), config.port.get(), window, listbox))
    go.grid(row=3, column=1)


def contacts_add_check(username, ip, port, window, listbox):
    """Для проверки никнейма и его добавления в список и отобразить."""
    for letter in username:
        if letter == " " or letter == "\n":
            base.control.error_window(root, "Неподходящее имя. Введите без "
                                            "пробелов.")
            return
    if base.control.check_options(window, ip):
        listbox.insert(tk.END, username + " " + ip + " " + port)
        config.contact_array[ip] = [port, username]
        window.destroy()
        return


def quick_client():
    """Окно для быстрого подключения."""
    window = tk.Toplevel(root)
    window.title("Настройки соединения")
    window.grab_set()
    tk.Label(window, text="IP адрес:").grid(row=0)
    destination = tk.Entry(window)
    destination.grid(row=0, column=1)
    go = tk.Button(window, text="Подключиться", command=lambda:
                   client_options_go(destination.get(), window))
    go.grid(row=1, column=1)


def save_history():
    """Сохранение истории чата."""
    file_name = asksaveasfilename(
        title="Выберите место сохранения",
        filetypes=[('Обычный текст', '*.txt'), ('Любой файл', '*.*')])
    try:
        file = open(file_name + ".txt", "w")
    except IOError:
        print("Невозможно сохранить историю.")
        return
    contents = config.main_body_text.get(1.0, tk.END)
    for line in contents:
        file.write(line)
    file.close()


def load_contacts():
    """Загрузка списка контактов."""
    try:
        file = open("contacts.dat", "r")
    except IOError:
        return
    line = file.readline()
    while len(line) != 0:
        temp = (line.rstrip('\n')).split(" ")
         # формат: ip, порт, имя
        config.contact_array[temp[0]] = temp[1:]
        line = file.readline()
    file.close()


def save_contacts():
    """Сохранение списка контактов."""
    try:
        file = open("contacts.dat", "w")
    except IOError:
        print("Can't dump contacts.")
        return
    for contact in config.contact_array:
        file.write(
            contact + " " + str(config.contact_array[contact][0]) + " " +
            config.contact_array[contact][1] + "\n")
    file.close()


def pars_text(event):
    """Парсинг текста из строки и проверка на команды, начинающиеся на '/'."""
    data = text_input.get()
    #если не команда
    if data[0] != "/":
        base.text.write_text(data)
    else:
        if data.find(" ") == -1:
            command = data[1:]
        else:
            command = data[1:data.find(" ")]
        params = data[data.find(" ") + 1:].split(" ")
        base.commands.user_commands(command, params, root)
    text_input.delete(0, tk.END)


root = tk.Tk()
root.title("Peer-2-Peer Чат")

first = tk.Frame(root)
second = tk.Frame(root)
main_body = tk.Frame(first, height=20, width=50)
input_body = tk.Frame(first, height=20, width=50)
contact_body = tk.Frame(second, height=20, width=50)
connect_body = tk.Frame(second, height=20, width=50)
contact_but = tk.Frame(contact_body, height=20, width=50)

config.main_body_text = tk.Text(main_body)

menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Сохранить чат", command=lambda: save_history())
file_menu.add_command(label="Сменить никнейм",
                      command=lambda: username_options_window(root))
file_menu.add_command(label="Выход", command=lambda: root.destroy())
menu_bar.add_cascade(label="Файл", menu=file_menu)
root.config(menu=menu_bar)


body_text_scroll = tk.Scrollbar(main_body)
config.main_body_text.focus_set()
body_text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
config.main_body_text.pack(side=tk.LEFT, fill=tk.Y)
body_text_scroll.config(command=config.main_body_text.yview)
config.main_body_text.config(yscrollcommand=body_text_scroll.set)
main_body.pack(side=tk.TOP)

config.main_body_text.insert(tk.END, "Добро пожаловать!")
config.main_body_text.config(state=tk.DISABLED)

text_input = tk.Entry(input_body, width=60)
text_input.bind("<Return>", pars_text)
text_input.pack()
input_body.pack(side=tk.BOTTOM)

connect_but = tk.Button(connect_body, text="Подключиться к...",
                        command=lambda: quick_client())
disconnect_but = tk.Button(connect_body, text="Отключение", command=lambda:
                           base.handler.event_handler("-001"))
connect_but.pack(side=tk.LEFT)
disconnect_but.pack(side=tk.RIGHT)
connect_body.pack(side=tk.TOP)

cont_scroll = tk.Scrollbar(contact_body, orient=tk.VERTICAL)
cont_listbox = tk.Listbox(contact_body, yscrollcommand=cont_scroll.set,
                          height=20)
cont_scroll.config(command=cont_listbox.yview)
cont_scroll.pack(side=tk.RIGHT, fill=tk.Y)

conn_but = tk.Button(contact_but, text="Подключиться", command=lambda:
                     contacts_connect(cont_listbox.get(tk.ACTIVE).split(" ")))
conn_but.pack(side=tk.LEFT)
del_but = tk.Button(contact_but, text="Удалить", command=lambda:
                    contacts_remove(cont_listbox.get(tk.ACTIVE).split(" "),
                                    cont_listbox))
del_but.pack(side=tk.LEFT)
add_but = tk.Button(contact_but, text="Добавить", command=lambda:
                    contacts_add(cont_listbox, root))
add_but.pack(side=tk.LEFT)
contact_but.pack(side=tk.BOTTOM)

load_contacts()
for person in config.contact_array:
        cont_listbox.insert(tk.END, str(config.contact_array[person][1]) + " "
                            "" + str(person) + " " +
                            str(config.contact_array[person][0]))

cont_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
contact_body.pack(side=tk.BOTTOM)

first.pack(side=tk.LEFT)
second.pack(side=tk.RIGHT)