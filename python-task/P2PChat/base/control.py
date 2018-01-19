__author__ = 'kowalski'
import config
import tkinter as tk
import base.text


def error_window(master, msg):
    """Запуск окна вывода ошибки."""
    if config.isCLI:
        base.text.write_to_screen(msg, "System")
    else:
        window = tk.Toplevel(master)
        window.title("ОШИБКА")
        window.grab_set()
        tk.Label(window, text=msg).pack()
        go = tk.Button(window, text="OK", command=window.destroy)
        go.pack()
        go.focus_set()


def check_options(root, loc=""):
    """Проверка адреса на правльность ввода. При ошибке выводиться
    окно собщения."""
    if loc != "":
        if not ip_check(loc.split(".")):
            if config.isCLI:
                error_window(0, "Пожалуйста введите правльный ip-адрес.")
            else:
                error_window(root, "Пожалуйста введите правльный ip-адрес.")
            return False
    return True


def ip_check(ip_array):
    """Проверка IP-адреса на валидность."""
    if len(ip_array) != 4:
        return False
    for ip in ip_array:
        if not ip.isnumeric():
            return False
        t = int(ip)
        if t < 0 or 255 < t:
            return False
    return True