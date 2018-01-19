__author__ = 'kowalski'
import config
import tkinter as tk
import base.net


def write_text(text):
    """Вывод текста из строки ввода и отправка сообщения всем, кто подключен"""
    write_to_screen(text, config.username)
    for person in config.send_array:
        base.net.net_throw(person, text)


def write_to_screen(text, username=""):
    """Основной вывод сообещения на экран в формате "Ник: Текст"."""
    if config.isCLI:
        if username:
            print(username + ": " + text)
        else:
            print(text)
    else:
        config.main_body_text.config(state=tk.NORMAL)
        config.main_body_text.insert(tk.END, '\n')
        if username:
            config.main_body_text.insert(tk.END, username + ": ")
        config.main_body_text.insert(tk.END, text)
        config.main_body_text.yview(tk.END)
        config.main_body_text.config(state=tk.DISABLED)