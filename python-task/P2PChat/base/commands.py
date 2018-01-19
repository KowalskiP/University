__author__ = 'kowalski'
import config
import base.control
import base.handler
import base.text
import base.net
import base.new_CSR


def user_commands(command, param, root=""):
    """Текстовые команды. Ввод через / ."""
    # смена никнейма
    if command == "nick":
        for letter in param[0]:
            if letter == " " or letter == "\n":
                base.control.error_window(root, "Неподходящее имя."
                                                " Введите без пробелов..")
                return
        if base.handler.is_username_free(param[0]):
            base.text.write_to_screen("Никнейм сменился на " + param[0],
                                      "System")
            for conn in config.send_array:
                conn.send("-002".encode(encoding='UTF-8'))
                base.net.net_throw(conn, param[0])
            config.username = param[0]
        else:
            base.text.write_to_screen(param[0] + " уже занято", "System")
    # отключение от текущего соединения
    if command == "disconnect":
        for conn in config.send_array:
            conn.send("-001".encode(encoding='UTF-8'))
        base.handler.event_handler("-001")
    # подключение к серверу
    if command == "connect":
        if base.control.check_options(0, param[0]):
            base.new_CSR.Client(param[0], config.port).start()


def pars_text_cli(text):
    """ClI version of processUserText."""
    if text[0] != "/":
        base.text.write_text(text)
    else:
        if text.find(" ") == -1:
            command = text[1:]
        else:
            command = text[1:text.find(" ")]
        params = text[text.find(" ") + 1:].split(" ")
        user_commands(command, params)